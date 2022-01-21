import json
import asyncio


class CacheStorage:
    def __init__(self, *, ttl: int = None):
        self.__cache = {}
        self.__ttl = ttl

    async def add(self, key: int, data: list, position=0) -> str:
        template = {
            "data": data,
            "position": position
        }
        self.__cache[key] = template
        return json.dumps(template)

    async def delete(self, chat_id) -> str:
        try:
            self.__cache.pop(chat_id)
        except KeyError as _ex:
            return "No user found"

    async def get_storage(self) -> dict:
        return self.__cache

    async def get_user(self, chat_id) -> dict:
        try:
            return self.__cache[chat_id]
        except KeyError as _ex:
            return dict()

    async def time_limit(self):
        pass

    async def increase(self, chat_id, amount=1) -> None:
        self.__cache[chat_id]["position"] += amount

    async def decrease(self, chat_id, amount=1) -> None:
        self.__cache[chat_id]["position"] -= amount


# tests #
async def test():
    cache = CacheStorage()
    await cache.add(228, [1, 1, 1, 1], position=0)
    asyncio.get_event_loop().run_until_complete(test())


def main(func):
    return func()


if __name__ == '__main__':
    print(main(test))
