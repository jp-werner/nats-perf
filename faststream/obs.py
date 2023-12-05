import aiofiles
from nats.js.object_store import ObjectStore
from typing_extensions import Annotated

from faststream import Context, FastStream, Logger
from faststream.nats import NatsBroker
from faststream.nats.annotations import ContextRepo
import anyio
import sys


bucket = "mybucket"
myfile = "wochendaemmerung.opus"


broker = NatsBroker()
app = FastStream(broker)

ObjectStorage = Annotated[ObjectStore, Context("OS")]


@app.on_startup
async def setup_broker(context: ContextRepo):
    await broker.connect()

    os = await broker.stream.create_object_store(bucket)
    context.set_global("OS", os)


@app.after_startup
async def test_send(os: ObjectStorage, logger: Logger):
    while True:
        try:
            async with aiofiles.open(myfile, "rb") as file:
                data = await file.read()
            up = await os.put("file", data)
            print(up)
        except FileNotFoundError:
            logger.error("File not found", exc_info=1)
            await anyio.CancelScope(shield=True).cancel()
            sys.exit(1)
