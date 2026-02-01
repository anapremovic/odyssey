import asyncio
import edge_tts

INPUT_TEXT = "I'm afraid I can't do that, Dave."
VOICE = "en-US-EricNeural"
OUTPUT_FILE = "test.wav"

async def amain() -> None:
    communicate = edge_tts.Communicate(INPUT_TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

if __name__ == "__main__":
    asyncio.run(amain())