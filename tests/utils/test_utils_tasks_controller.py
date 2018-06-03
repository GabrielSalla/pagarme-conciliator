from src.utils.tasks_controller import TasksController
import pytest
import asyncio
import time
import math
import random

pytestmark = pytest.mark.asyncio


def get_numbers():
    return (random.randrange(1, 100), random.randrange(1, 100))


async def slow_sum(a, b):
    await asyncio.sleep(0.1)
    return a + b


# A task should only execute after ensureing it's future
async def test_ensure_future():
    result = []

    async def append_result():
        result.append(1)

    task = append_result()
    await asyncio.sleep(0.01)
    assert len(result) == 0
    asyncio.ensure_future(task)
    await asyncio.sleep(0.01)
    assert len(result) == 1


# wait() should not break if no tasks were queued
async def test_wait_empty():
    flux_controller = TasksController(5)
    start_time = time.time()
    await flux_controller.wait()
    end_time = time.time()
    # Assert the spent time is small
    assert end_time - start_time < 0.01


# gather() should not break and return an empty list if no tasks were queued
async def test_gather_empty():
    flux_controller = TasksController(5)
    start_time = time.time()
    results = await flux_controller.gather()
    end_time = time.time()
    # Assert the spent time is small
    assert end_time - start_time < 0.01
    assert isinstance(results, list)
    assert len(results) == 0


# run() should wait for a slot to run and wait() should wait for all tasks to
# finish
async def test_wait_run_1():
    flux_controller = TasksController(5)
    start_time = time.time()
    # Run the tasks from 0.1s to 1s (10 different times)
    for wait_time in range(1, 11, 1):
        await flux_controller.run(asyncio.sleep(wait_time/10.))
    # Wait for all the tasks to finish
    await flux_controller.wait()
    end_time = time.time()
    # Assert the spent time is right (the slot that will take the longest to
    # finish is the one who will wait for 0.5s and 1s)
    assert 1.5 < end_time - start_time < 1.6


# run() should wait for a slot to run and wait() should wait for all tasks to
# finish
@pytest.mark.parametrize("n, size", [
    (1, 1),
    (2, 1),
    (5, 5),
    (20, 5),
    (20, 20)
])
async def test_wait_run_2(n, size):
    flux_controller = TasksController(size)
    start_time = time.time()
    # Run the tasks
    for _ in range(n):
        await flux_controller.run(asyncio.sleep(0.1))
    # Wait for all the tasks to finish
    await flux_controller.wait()
    end_time = time.time()
    expected_min_time = 0.1 * (1 + math.floor((n - 1) / size))
    expected_max_time = expected_min_time * 1.2
    # Assert the spent time is right
    assert expected_min_time < end_time - start_time < expected_max_time


# gather() should wait for all tasks to finish and return the results
@pytest.mark.parametrize("n, size", [
    (1, 1),
    (2, 1),
    (5, 5),
    (20, 5),
    (20, 20)
])
async def test_gather_run(n, size):
    flux_controller = TasksController(size)
    expected_results = []
    start_time = time.time()
    # Run the tasks
    for _ in range(n):
        a, b = get_numbers()
        expected_results.append(a + b)
        await flux_controller.run(slow_sum(a, b))
    # Wait for all the tasks to finish and get the results
    results = await flux_controller.gather()
    end_time = time.time()
    expected_min_time = 0.1 * (1 + math.floor((n - 1) / size))
    expected_max_time = expected_min_time * 1.2
    # Assert the spent time is right
    assert expected_min_time < end_time - start_time < expected_max_time
    # Assert the results are right
    assert results == expected_results


# run_all() should return instantly and should queue taks in the background
# wait() should wait for all the tasks to be queued and all the queued tasks to
# finish
@pytest.mark.parametrize("n, size", [
    (1, 1),
    (2, 1),
    (5, 5),
    (20, 5),
    (20, 20)
])
async def test_wait_run_all(n, size):
    flux_controller = TasksController(size)
    tasks_queue = []
    # Run the tasks
    for _ in range(n):
        tasks_queue.append(asyncio.sleep(0.1))
    start_time = time.time()
    # Queue the tasks to run in the background
    flux_controller.run_all(tasks_queue)
    after_queue_time = time.time()
    # Wait for all the tasks to finish
    await flux_controller.wait()
    end_time = time.time()
    expected_min_time = 0.1 * (1 + math.floor((n - 1) / size))
    expected_max_time = expected_min_time * 1.2
    # Assert the time to queue the tasks is small
    assert after_queue_time - start_time < 0.01
    # Assert the spent time is right
    assert expected_min_time < end_time - start_time < expected_max_time


# gather() should wait for all the tasks to be queued and all the queued tasks
# to finish
@pytest.mark.parametrize("n, size", [
    (1, 1),
    (2, 1),
    (5, 5),
    (20, 5),
    (20, 20)
])
async def test_gather_run_all(n, size):
    flux_controller = TasksController(size)
    expected_results = []
    tasks_queue = []
    # Run the tasks
    for _ in range(n):
        a, b = get_numbers()
        expected_results.append(a + b)
        tasks_queue.append(slow_sum(a, b))
    start_time = time.time()
    # Queue the tasks to run in the background
    flux_controller.run_all(tasks_queue)
    after_queue_time = time.time()
    # Wait for all the tasks to finish
    results = await flux_controller.gather()
    end_time = time.time()
    expected_min_time = 0.1 * (1 + math.floor((n - 1) / size))
    expected_max_time = expected_min_time * 1.2
    # Assert the time to queue the tasks is small
    assert after_queue_time - start_time < 0.01
    # Assert the spent time is right
    assert expected_min_time < end_time - start_time < expected_max_time
    # Assert the results are right
    assert results == expected_results


# run_all() should work if called multiple times
# wait() should wait for all the tasks to be queued and all the queued tasks to
# finish
@pytest.mark.parametrize("n, size", [
    (1, 1),
    (2, 1),
    (5, 5),
    (20, 5),
    (20, 20)
])
@pytest.mark.parametrize("repeat_number", [1, 2, 3, 4])
async def test_run_all_multiple(n, size, repeat_number):
    flux_controller = TasksController(size)
    start_time = time.time()
    # Create and queue the tasks to run in the background
    for _ in range(repeat_number):
        tasks_queue = [asyncio.sleep(0.1) for _ in range(n)]
        flux_controller.run_all(tasks_queue)
    after_queue_time = time.time()
    # Wait for all the tasks to finish
    await flux_controller.wait()
    end_time = time.time()
    expected_min_time = 0.1 * (1 + math.floor((n * repeat_number - 1) / size))
    expected_max_time = expected_min_time * 1.2
    # Assert the time to queue the tasks is small
    assert after_queue_time - start_time < 0.01
    # Assert the spent time is right
    assert expected_min_time < end_time - start_time < expected_max_time
