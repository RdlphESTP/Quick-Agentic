import logging

import chainlit as cl
from chainlit.input_widget import Slider, Switch
from langgraph_sdk import get_client
from template.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

client = get_client(url="http://localhost:2024")

ASSISTANT_ID = "agent"


# ////////////////////////////////// SESSION START \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@cl.on_chat_start
async def start_chat():
    thread = await client.threads.create()

    cl.user_session.set("thread_id", thread["thread_id"])

    # Add selectable commands to the chat bar
    await cl.context.emitter.set_commands(
        [
            {
                "id": "Generic Param",
                "icon": "waypoints",
                "description": "Generic Description",
                "button": True,
                "persistent": False,
                "selected": False,
            },
        ]
    )

    # Define Agent Settings
    await cl.ChatSettings(
        [
            Slider(id="TBD1", label="Generic Slider"),
            Switch(id="TBD2", label="Generic Switch"),
        ]
    ).send()
    logger.info("New Chat session started")


# //////////////////////////////// START PAGE CARDS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@cl.set_starters
async def starters(
    current_user: cl.User | None, chat_profile: str | None
) -> list[cl.Starter]:
    # Add Starter Cards under the chat bar
    return [
        cl.Starter(label="Generic Card", message="", command="TBD3"),
    ]


# ///////////////////////////////// AGENT SETTINGS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@cl.on_settings_edit
async def on_edit(settings):
    # Update Agent Settings
    inputs = [
        Slider(id="TBD1", label="Generic Slider", initial=settings.get("TBD1", 0)),
        Switch(id="TBD2", label="Generic Switch", initial=settings.get("TBD2", 0)),
    ]
    await cl.ChatSettings(inputs).refresh()


@cl.on_settings_update
async def on_update(settings):
    logger.info("Selected parameters : %s", settings)


# ////////////////////////////////////// CORE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@cl.on_message
async def main(prompt: cl.Message):
    thread_id = cl.user_session.get("thread_id")

    llm_msg = cl.Message(content="")
    await llm_msg.send()

    async with cl.Step(name="Thinking", type="run") as step:
        step.icon = "hourglass"
        await step.update()

        async for chunk in client.runs.stream(
            thread_id,
            ASSISTANT_ID,
            input={"messages": [{"role": "user", "content": prompt.content}]},
            stream_mode=["messages-tuple", "custom"],
        ):
            if chunk.event == "messages":
                message_chunk, _ = chunk.data

                content = message_chunk.get("content")

                if content:
                    await llm_msg.stream_token(content)

            elif chunk.event == "custom":
                print(chunk.event, chunk.data)
                data = chunk.data

                step.name = data["name"]
                step.icon = data["icon"]

                await step.update()

    await llm_msg.update()
    await step.remove()


# ////////////////////////////////////// EXIT \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@cl.on_stop
def on_stop():
    logger.info("Chat interrupted by user.")


@cl.on_chat_end
def on_chat_end():
    logger.info("Chat session ended.")
