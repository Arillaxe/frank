from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.audio import audio_test
from src.eventHandler import EventHandler
from .openai import client, assistant

class Message(BaseModel):
    text: str

app = FastAPI()

@app.post("/message")
async def root(message: Message):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message.text,
    )

    async def stream_generator():
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=EventHandler()
        ) as stream:
            for text in stream.text_deltas:
                yield text
            stream.until_done()

    return StreamingResponse(stream_generator(), media_type='text/event-stream')

@app.get('/audio_test')
def audio():
    audio_test()
    return 2
