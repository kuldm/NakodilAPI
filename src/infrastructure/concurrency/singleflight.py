import asyncio

class Singleflight:
    def __init__(self):
        self._tasks = {}

    async def run(self, key: str, operation):
        if key in self._tasks:
            task = self._tasks[key]

        else:
            task = asyncio.create_task(self._executor(operation, key))
            self._tasks[key] = task

        return await asyncio.shield(task)

    async def _executor(self, operation, key):
        try:
            result = await operation
        finally:
            del self._tasks[key]

        return result