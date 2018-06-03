import src.conciliator as conciliator
import src.models as models
import datetime


async def all():
    await conciliator.fetch_balance_operations({"start_date": 0})
    await conciliator.fetch_recipients()
    await conciliator.fetch_bulk_anticipations()
    await conciliator.fetch_transactions({"date_created": ">0"})


async def new():
    # BalanceOperations
    last_balance_operation = await models.BalanceOperation.async_last(
        models.BalanceOperation.created_at)
    # Subtract 1 hour from the timestamp to avoid problems with things that
    # were too new when the previous conciliation was executed
    operation_timestamp = int((
        last_balance_operation.created_at -
        datetime.timedelta(hours=1)
    ).timestamp() * 1000)
    await conciliator.fetch_balance_operations(
        {"start_date": operation_timestamp})

    # Recipients
    await conciliator.fetch_recipients()

    # BulkAnticipations
    await conciliator.fetch_bulk_anticipations()

    # Transactions
    last_transaction = await models.Transaction.async_last(
        models.Transaction.updated_at)
    # Subtract 1 hour from the timestamp to avoid problems with things that
    # were too new when the previous conciliation was executed
    transaction_timestamp = int((
        last_transaction.updated_at -
        datetime.timedelta(hours=1)
    ).timestamp() * 1000)
    await conciliator.fetch_transactions(
        {"date_updated": f">{transaction_timestamp}"})
