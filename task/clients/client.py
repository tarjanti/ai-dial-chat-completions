from aidial_client import Dial, AsyncDial
from task.constants import API_KEY
from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._dial_client = Dial(api_key=API_KEY, base_url=DIAL_ENDPOINT)
        self._async_dial_client = AsyncDial(api_key=API_KEY, base_url=DIAL_ENDPOINT)

    def get_completion(self, messages: list[Message]) -> Message:
        completion = self._dial_client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=False,
            messages=[message.to_dict() for message in messages]
        )
        return Message(Role.AI, completion.choices[0].message.content)

    async def stream_completion(self, messages: list[Message]) -> Message:
        chunks = await self._async_dial_client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=True,
            messages=[message.to_dict() for message in messages]
        )
        contents = []
        async for chunk in chunks:
            choices = chunk.choices
            if choices and len(choices) > 0:
                delta = choices[0].delta
                if delta and delta.content:
                    print(delta.content, end="")
                    contents.append(delta.content)
        print()
        return Message(Role.AI, "".join(contents))
