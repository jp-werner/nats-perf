from datetime import datetime

from faststream import FastStream, Logger
from faststream.nats import JStream, NatsBroker, PullSub

broker = NatsBroker()
app = FastStream(broker)


stream = JStream(name="mystream")
subject = "mysubject"

subscriber_name = "mysubscriber"


@broker.subscriber(
    subject=subject, stream=stream, pull_sub=PullSub(batch_size=10), durable=subscriber_name
)
async def handler(msg: str, logger: Logger):
    logger.info(msg)


@app.after_startup
async def test_send():
    while True:
        await broker.publish(f"TS: {datetime.now()}", subject)
