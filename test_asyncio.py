import asyncio

async def hello():
    print("Hello World!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello())
