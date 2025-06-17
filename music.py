import asyncio
import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY
import traceback

async def main():
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set in environment variables.")
        print("Please set the GEMINI_API_KEY environment variable.")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)

    async def receive_audio(session):
        """Background task to process incoming audio."""
        print("Starting audio reception...")
        try:
            async for message in session.receive():
                if message.server_content and message.server_content.audio_chunks:
                    audio_data = message.server_content.audio_chunks[0].data
                    # In a real application, you would play this audio.
                    # For this example, we'll just print its size.
                    print(f"Received audio chunk of size: {len(audio_data)} bytes")
                elif message.filtered_prompt:
                    print(f"Filtered prompt: {message.filtered_prompt.text} - Reason: {message.filtered_prompt.filtered_reason}")
                elif message.setup_complete:
                    print("Session setup complete.")
                else:
                    print(f"Received other message: {message}")
                await asyncio.sleep(10**-12) # Yield control to other tasks
        except Exception as e:
            print(f"Error within receive_audio task: {e}")
            traceback.print_exc() # Print full traceback for this task
            raise # Re-raise to ensure TaskGroup catches it if it's the root cause

    try:
        # Define the LiveConnectConfig to request audio responses
        live_config = types.LiveConnectConfig(
            response_modalities=["AUDIO"]
        )

        async with (
            client.aio.live.connect(model='gemini-2.5-flash-preview-native-audio-dialog', config=live_config) as session,
            asyncio.TaskGroup() as tg,
        ):
            print("Connected to Live Audio session with gemini-2.5-flash-preview-native-audio-dialog.")
            
            # Create the receive audio task
            audio_task = tg.create_task(receive_audio(session))

            print("Attempting to set initial prompts (currently commented out for debugging)...")
            # await session.set_weighted_prompts(
            #     prompts=[
            #         types.WeightedPrompt(text='minimal techno', weight=1.0),
            #     ]
            # )
            print("Attempting to set music generation config (currently commented out for debugging)...")
            # await session.set_music_generation_config(
            #     config=types.LiveMusicGenerationConfig(bpm=120, temperature=1.0)
            # )

            print("Calling session.play()...")
            try:
                await session.play()
                print("session.play() successful. Listening for audio...")
            except Exception as e:
                print(f"Error during session.play(): {e}")
                traceback.print_exc()
                # If play fails, the audio_task might also fail or not receive anything.
                # Propagate this error to the TaskGroup to get the full traceback.
                raise

            print("Listening for 10 seconds of music...")
            await asyncio.sleep(10)

            print("Pausing music...")
            await session.pause()
            print("Music paused. Waiting 2 seconds...")
            await asyncio.sleep(2)

            print("Resuming music...")
            await session.play()
            print("Music resumed. Listening for another 5 seconds...")
            await asyncio.sleep(5)

            print("Stopping music and resetting context...")
            await session.stop()
            await session.reset_context()
            print("Session stopped and context reset.")

    except Exception as e:
        print(f"An error occurred in the main session: {e}")
        traceback.print_exc() # Print full traceback for the main session error

if __name__ == "__main__":
    print("Running Lyria RealTime music generation test...")
    asyncio.run(main()) 