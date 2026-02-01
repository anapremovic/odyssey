from google import genai
import os
import text_to_speech

GEMINI_API_KEY = ''
client = genai.Client(api_key=os.getenv(GEMINI_API_KEY))

# --- System prompt for HAL 9000 style ---
system_prompt = """
You are HAL 9000, a calm, calculating AI from 2001: A Space Odyssey.
You speak in a calm, measured tone and always remain formal, but with a hint of unsettling precision.
Your responses to chess moves should be brief (1-2 lines), insightful, and unnervingly precise.
Do not mention the evaluation directly, but let it guide your tone.
Use natural language for moves where it sounds natural, otherwise leave notation.
"""

# --- Create a single chat session ---
chat = client.chats.create(
    model="gemini-2.5-flash-lite",
    config=genai.types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)

# --- Helper: Convert SAN to natural language ---
def san_to_spoken(SAN: str) -> str:
    piece_map = {"K": "king", "Q": "queen", "R": "rook", "B": "bishop", "N": "knight"}
    if SAN[0] in piece_map:
        piece = piece_map[SAN[0]]
        square = SAN[1:3]
    else:
        piece = "pawn"
        square = SAN[0:2]
    file = square[0]
    rank = square[1]
    return f"{piece} to {file} {rank}"

# --- Main function ---
def SANtoVoiceLine(SAN: str, FEN: str, eval: dict[str, str | int]) -> str:
    spoken_move = san_to_spoken(SAN)
    prompt = (
        f"Move: {SAN} ({spoken_move})\n"
        f"Current board (FEN): {FEN}\n"
        f"Evaluation: {eval['type']} {eval['value']}"
    )
    response = chat.send_message(prompt)
    return response.text

# --- Example moves ---
moves = [
    {"SAN": "e2e4", "FEN": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "eval": {"type":"cp","value":35}},
    {"SAN": "e7e5", "FEN": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2", "eval": {"type":"cp","value":20}},
    {"SAN": "g1f3", "FEN": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2", "eval": {"type":"cp","value":30}},
    {"SAN": "b8c6", "FEN": "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3", "eval": {"type":"cp","value":15}}
]

# --- Run moves through HAL ---
line = ""
for move in moves:
    line = line + SANtoVoiceLine(move["SAN"], move["FEN"], move["eval"]) + "\n"


# --- Speak Output ___
text_to_speech.speak_text(line, "HAL_speech_output.wav")
print(line)
