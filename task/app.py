import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role

USER_INPUT_PROMPT = "> "


async def start(stream: bool) -> None:
    dial_client = DialClient("gpt-4o")
    custom_dial_client = CustomDialClient("gpt-4o")
    conversation = Conversation()

    print("Provide System prompt or press 'enter' to continue.")
    system_prompt = input(USER_INPUT_PROMPT).strip()
    if system_prompt:
        conversation.add_message(Message(Role.SYSTEM, system_prompt))
        print("System prompt was added to the conversation.")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(f"The default system prompt was added to the conversation: {DEFAULT_SYSTEM_PROMPT}")
    print()

    print("Type your question or 'exit' to quit.")
    while True:
        user_input = input(USER_INPUT_PROMPT).strip()
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        conversation.add_message(Message(Role.USER, user_input))

        if stream:
            ai_response_message = await custom_dial_client.stream_completion(conversation.get_messages())
        else:
            ai_response_message = custom_dial_client.get_completion(conversation.get_messages())

        conversation.add_message(ai_response_message)


asyncio.run(
    start(True)
)
