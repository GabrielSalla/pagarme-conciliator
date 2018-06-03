import src.prod_database as prod_database_controller
import src.conciliation_operations as conciliation_operations
import src.pagarme_api as pagarme_api
import src.utils.time as time_utils
import logging
import traceback
import asyncio
import sys
import os

TIME_FORMAT = "%y-%m-%d_%H:%M:%S"
FILE_NAME = time_utils.now_br().strftime(TIME_FORMAT) + ".log"
FILE_PATH = os.path.join(".", "logs", FILE_NAME)
LOG_FORMAT = "[%(asctime)s] (%(levelname)s) %(name)s: %(message)s"
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO,
    handlers=[
        logging.FileHandler(FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)
_logger = logging.getLogger("Core")
_running = True


async def _finish():
    try:
        prod_database_controller.close_connections()
    except Exception:
        _logger.error(traceback.format_exc())


async def start():
    authenticated = await pagarme_api.authenticate()
    if not authenticated:
        return
    try:
        operation = sys.argv[1]
    except IndexError:
        _logger.error("Missing operation parameter")
        return
    operation_function = getattr(conciliation_operations,  operation, None)
    if operation_function is None:
        _logger.error(f"Invalid operation {operation}")
        return
    try:
        await operation_function()
    finally:
        await _finish()


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if(__name__ == "__main__"):
    main()
