import asyncio
import aiosqlite
import json
import datetime
from aiokafka import AIOKafkaProducer
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "")
KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "")


class Producer:
    def __init__(self, db_path: str = DATABASE_PATH, kafka_server: str = KAFKA_SERVER):
        self.db_path = db_path
        self.kafka_server = kafka_server
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.kafka_server,
            value_serializer=lambda v: json.dumps(v).encode(),
            key_serializer=lambda k: k.encode() if k else None,
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def fetch_pending_cases(self):
        query = "SELECT uuid FROM ascvts_case WHERE description is NULL or description = '' LIMIT 100 OFFSET ({page} - 1) * 100"
        page = 1
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            while True:
                async with conn.execute(query.format(page=page)) as cursor:
                    rows = await cursor.fetchall()
                    if not rows:
                        break
                    yield [dict(row) for row in rows]
                    page += 1

    async def publish_case(self, case):
        await self.producer.send_and_wait(
            "case.pending",
            value={
                "uuid": case["uuid"],
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            },
        )
        return case["uuid"]

    async def run(self):
        await self.start()
        try:
            async for batch in self.fetch_pending_cases():
                for case in batch:
                    await self.publish_case(case)
        except Exception as e:
            print("Something went wrong:", str(e))
        finally:
            await self.stop()


async def main():
    await Producer().run()


if __name__ == "__main__":
    asyncio.run(main())
