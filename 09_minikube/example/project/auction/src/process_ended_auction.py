import asyncio
import logging


async def process_ended_auction() -> None:
    logging.info("[process_ended_auction] started")
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(process_ended_auction())



