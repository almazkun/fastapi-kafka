import asyncio
import sqlite3
import json
import datetime
from aiokafka import AIOKafkaProducer
from contextlib import closing
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

    def fetch_pending_cases(self):
        query = """
            SELECT uuid 
            FROM ascvts_case
            WHERE description is NULL or description = ''
            LIMIT 100
        """
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

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
            cases = self.fetch_pending_cases()
            print("Found cases:", len(cases), cases[0])
            for case in cases:
                event = await self.publish_case(case)
                print("Case published", event)
            print("Done")
        except Exception as e:
            print("Something went wrong:", str(e))
        finally:
            await self.stop()


async def main():
    fetcher = Producer()
    await fetcher.run()


if __name__ == "__main__":
    asyncio.run(main())
