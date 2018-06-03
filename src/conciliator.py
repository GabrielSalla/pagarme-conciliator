import src.models as models
import src.pagarme_api as pagarme_api
from src.utils.tasks_controller import TasksController
import asyncio
import logging
import time

_logger = logging.getLogger("Conciliator")

objects_mapper = {
    "address": models.Address,
    "balance_operation": models.BalanceOperation,
    "bank_account": models.BankAccount,
    "bulk_anticipation": models.BulkAnticipation,
    "card": models.Card,
    "customer": models.Customer,
    "fee_collection": models.FeeCollection,
    "invoice": models.Invoice,
    "payable": models.Payable,
    "phone": models.Phone,
    "recipient": models.Recipient,
    "split_rule": models.SplitRule,
    "transaction": models.Transaction,
    "transfer": models.Transfer,
}

nest_fields = (
    "address",
    "bank_account",
    "card",
    "customer",
    "movement_object",
    "phone",
    "split_rules"
)


# Decorato to set dependencies that should be executed before
def depends_on(dependencies_functions=()):
    def real_decorator(function):
        async def wrapper(*args, skip_dependencies=False, **kwargs):
            if not skip_dependencies:
                for task in dependencies_functions:
                    await task()
            await function(*args, **kwargs)
        return wrapper
    return real_decorator


# Decorato to set triggers that should be executed after
def triggers(trigger_functions=()):
    def real_decorator(function):
        async def wrapper(*args, skip_triggers=False, **kwargs):
            await function(*args, **kwargs)
            if not skip_triggers:
                for task in trigger_functions:
                    await task()
        return wrapper
    return real_decorator


def get_identificator(obj):
    # Adapting to error in the api where the object is fee_collection when it's
    # really an invoice
    if obj["object"] == "fee_collection" and obj["id"].startswith("in_"):
        return ("invoice", obj["id"])
    return (obj["object"], obj["id"])


# Recursive function to inspect the objects and it's nested objects to identify
# everything that should be managed later
def dicover_objects(obj):
    objects = dict()

    if isinstance(obj, list):
        for item in obj:
            objects.update(dicover_objects(item))
        return objects
    if not isinstance(obj, dict):
        _logger.error(f"Invalid object to process {obj}")

    identificator = get_identificator(obj)
    # Compare if there's an existing object with the same identification to be
    # processed with different data. No action is being taken right now, but
    # logs a warning
    try:
        saved_obj = objects[identificator]
        if saved_obj != obj:
            _logger.warning(
                f"Inconsistent data for object {identificator}\n"
                f"{saved_obj}\n"
                f"{obj}"
            )
        else:
            objects[identificator] = obj
    except KeyError:
        objects[identificator] = obj

    # Process nested objects
    for field in nest_fields:
        try:
            nested_object = obj[field]
            if nested_object is not None:
                objects.update(dicover_objects(nested_object))
        except KeyError:
            pass

    return objects


async def process_object(obj):
    objects = dicover_objects(obj)
    flux_controller = TasksController(5)
    for (model, model_id), data in objects.items():
        target_class = objects_mapper[model]
        _logger.info(f"Processing {target_class.__name__} {model_id}")
        await flux_controller.run(target_class.manage_data(data))
    await flux_controller.wait()


# Do a paginated fetch with a buffer of requests to increase the speed
async def paginated_fetch(endpoint, params=None, queue_size=5):
    page_size = 100
    page = 1

    # Crate the first tasks of the list
    queue = list()
    for _ in range(queue_size):
        request_params = dict(
            count=page_size,
            page=page
        )
        if params is not None:
            request_params.update(params)
        # Let the tasks running in the background
        queue.append(asyncio.ensure_future(
            pagarme_api.get(endpoint, request_params)))
        page += 1

    # After the buffer is created, pop the first item of the queue, wait for it
    # to finish, queue a new task and yield the result
    # This way the queue will be generated and executed in the background,
    # while the application is using the yielded item
    while True:
        result = await queue.pop(0)
        # Only queue a new task if is returning a full list, and before
        # yielding the result
        if len(result) == page_size:
            queue.append(asyncio.ensure_future(
                pagarme_api.get(endpoint, request_params)))
        yield result
        if len(result) < page_size:
            # Wait for all the queued tasks to finish
            await asyncio.wait(queue)
            return
        request_params["page"] += 1


async def fetch_balance_operations(fetch_params):
    _logger.info("Conciliating BalanceOperations")
    fetch_task = paginated_fetch(
        models.BalanceOperation.ENDPOINT,
        fetch_params
    )
    async for balance_operation_list in fetch_task:
        await process_object(balance_operation_list)


async def fetch_recipients():
    _logger.info("Conciliating Recipients")
    fetch_task = paginated_fetch(models.Recipient.ENDPOINT)
    async for recipient_list in fetch_task:
        await process_object(recipient_list)


async def fetch_recipient_anticipations(recipient):
    _logger.info(f"Fetching anticipations for {recipient.id}")
    endpoint = models.BulkAnticipation.ENDPOINT.format(
        recipient_id=recipient.id)
    # Using a small queue size because there shouldn't be a lot of
    # anticipations for each recipient
    fetch_task = paginated_fetch(endpoint, queue_size=1)
    async for bulk_anticipation_list in fetch_task:
        # Using a for loop instead of processing the objects as the
        # recipient_id must be inserted
        for bulk_anticipation in bulk_anticipation_list:
            bulk_anticipation["recipient_id"] = recipient.id
            await manage_pending_objects(bulk_anticipation)


# @depends_on((fetch_recipients,))
async def fetch_bulk_anticipations():
    _logger.info("Conciliating BulkAnticipations")
    flux_controller = TasksController(5)
    recipients = await models.Recipient.async_select()
    for recipient in recipients:
        await flux_controller.run(fetch_recipient_anticipations(recipient))
    await flux_controller.wait()


async def fetch_transactions(fetch_params):
    _logger.info("Conciliating Transactions")
    fetch_task = paginated_fetch(
        models.Transaction.ENDPOINT,
        fetch_params
    )
    async for transaction_list in fetch_task:
        await process_object(transaction_list)
