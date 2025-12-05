import os
import asyncio
import json
import datetime
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "")
INPUT_TOPIC = "case.pending"
OUTPUT_TOPIC = "case.context"
DOCKER_CONTAINER = os.environ.get("DOCKER_CONTAINER", "")


async def run_docker_run(uuid: str, contained_id: str = DOCKER_CONTAINER) -> dict:
    proc = await asyncio.create_subprocess_exec(
        "docker",
        "exec",
        contained_id,
        f"python run manage.py case_json {uuid}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = proc.communicate()
    print(stderr[:10])
    print(stdout[:10])
    if proc.returncode != 0:
        return RuntimeError(f"Error: {stderr.decode().strip()}")
    return json.loads(stdout.decode())


async def main():
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode()),
        group_id="case_context_group",
    )
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode(),
    )

    await consumer.start()
    await producer.start()

    try:
        async for msg in consumer:
            uuid = msg.value["uuid"]
            case_json = await run_docker_run(uuid)
            await producer.send_and_wait(
                OUTPUT_TOPIC,
                {
                    "uuid": msg["uuid"],
                    "context": case_json,
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                },
            )
    except Exception as e:
        print("Fails", msg, str(e))
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
