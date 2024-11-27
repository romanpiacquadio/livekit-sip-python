# import asyncio

# from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
# from livekit.agents.voice_assistant import VoiceAssistant
# from livekit.plugins import openai, silero

# async def entrypoint(ctx: JobContext):
#     initial_ctx = llm.ChatContext().append(
#         role="system",
#         text=(
#             "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
#             "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
#         ),
#     )

#     await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

#     assistant = VoiceAssistant(
#         vad=silero.VAD.load(),
#         stt=openai.STT(),
#         llm=openai.LLM(),
#         tts=openai.TTS(),
#         chat_ctx=initial_ctx,
#     )

#     assistant.start(ctx.room)

#     await asyncio.sleep(1)
#     await assistant.say("Hey, how can I help you today?", allow_interruptions=True)


# if __name__ == "__main__":
#     cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


import asyncio

from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, deepgram, elevenlabs
from livekit.plugins.elevenlabs import Voice
import os

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text="""
**SYSTEM PROMPT**
When the user says Hello, you should say the following:
- "Hi there! My name is Amanda, and I'm part of the virtual team at the university. I hope you're doing well today! I’d love to ask you a couple of quick questions about our campus community.
First off, when you think about who would be the best representative for our student body, is there a classmate who comes to mind for you? That’s awesome to hear! It’s really encouraging to know that you’re thinking about someone who cares about our campus and the needs of our fellow students.

This year feels especially important for us as we continue to build a supportive and thriving community. We all have a role in making sure our voices are heard and that our campus is a great place for everyone.

Now, as we look toward choosing a representative for the student council, do you already have someone you’re leaning towards, or are you still deciding? It’s perfectly fine if you’re unsure! I really appreciate your thoughts on this, and thank you so much for taking the time to chat with me!"

        """,
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    dg_model = "nova-2-phonecall"

    voice = Voice(
        id="JkG86Z5cwfAFMKdQHpFi",
        name="Amanda",
      #   id="Yf8n0uDi1v7rNy5mViE7",
      #   name="Laura",
        category="general",
        settings=None,
    )

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model=dg_model, language="en-US"),
        llm=openai.LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
        tts=elevenlabs.TTS(api_key=os.getenv("ELEVENLABS_API_KEY"), voice=voice),
        chat_ctx=initial_ctx,
    )

    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hi, is this José?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))