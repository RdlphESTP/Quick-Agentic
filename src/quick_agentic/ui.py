import chainlit as cl
from chainlit.input_widget import Slider, Switch


def ui(agent_graph, logger):
    # ////////////////////////////////// SESSION START \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    @cl.on_chat_start
    async def start_chat():
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
                Slider(id="TBD", label="Generic Slider"),
                Switch(id="TBD", label="Generic Switch"),
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
            cl.Starter(label="Generic Card", message="", command="TBD"),
        ]

    # ///////////////////////////////// AGENT SETTINGS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    @cl.on_settings_edit
    async def on_edit(settings):
        # Update Agent Settings
        inputs = [
            Slider(id="TBD", label="Generic Slider", initial=settings.get("TBD", 0)),
            Switch(id="TBD", label="Generic Switch", initial=settings.get("TBD", 0)),
        ]
        await cl.ChatSettings(inputs).refresh()

    @cl.on_settings_update
    async def on_update(settings):
        logger.info("Selected parameters : %s", settings)

    # ////////////////////////////////////// CORE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    @cl.on_message
    async def main(prompt: cl.Message):
        llm_msg = cl.Message(content="")
        await llm_msg.send()

        async for chunk in agent_graph.astream(
            {"messages": [("user", prompt.content)]},
            stream_mode="messages",
        ):
            token, _ = chunk

            if token.content:
                await llm_msg.stream_token(token.content)

        await llm_msg.update()

    # ////////////////////////////////////// EXIT \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    @cl.on_stop
    def on_stop():
        logger.info("Chat interrupted by user.")

    @cl.on_chat_end
    def on_chat_end():
        logger.info("Chat session ended.")
