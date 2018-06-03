import asyncio


# Class to control the number of tasks running concurrently
# If there's an uncaught exception in one of the running tasks, the returned
# value of the task will be it's exception object
class TasksController():
    def __init__(self, size):
        self._semaphore = asyncio.Semaphore(size)
        self._queue_tasks = []
        self._tasks = []

    async def _background_run(self, task):
        try:
            return await task
        except Exception as exception:
            return exception
        finally:
            self._semaphore.release()

    # Run a single task in the background
    async def run(self, task):
        await self._semaphore.acquire()
        try:
            self._tasks.append(asyncio.ensure_future(
                self._background_run(task)))
        except Exception as exception:
            self._semaphore.release()
            raise exception

    async def _background_queue(self, tasks_list):
        for task in tasks_list:
            await self.run(task)

    # Create background task that will run all the tasks in the background
    def run_all(self, tasks_list):
        self._queue_tasks.append(asyncio.ensure_future(
            self._background_queue(tasks_list)))

    # Wait for all the tasks to finish
    async def wait(self):
        if len(self._queue_tasks) > 0:
            await asyncio.wait(self._queue_tasks)
        if len(self._tasks) > 0:
            await asyncio.wait(self._tasks)

    # Gather the results of all the tasks
    async def gather(self):
        if len(self._queue_tasks) > 0:
            await asyncio.wait(self._queue_tasks)
        if len(self._tasks) > 0:
            return await asyncio.gather(*self._tasks)
        return []

    # Get all the exceptions that were raised in the tasks
    async def get_exceptions(self):
        if len(self._queue_tasks) > 0:
            await asyncio.wait(self._queue_tasks)
        if len(self._tasks) > 0:
            results = await asyncio.gather(*self._tasks)
            return list(filter(
                lambda result: isinstance(result, Exception), results))
        return []

    # Clear the tasks list
    def clear(self):
        self._queue_tasks = []
        self._tasks = []
