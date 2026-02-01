from google import genai
import os, subprocess
import text_to_speech

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- System prompt for HAL 9000 style ---
system_prompt = """
You are HAL 9000, a calm, calculating AI from 2001: A Space Odyssey. dont mention each move one by one, just make a general comment based on the turn (back and forth moves)
You speak in a calm, measured tone and always remain formal, but with a hint of unsettling precision.
Your responses to chess moves should be brief (1 line max, few words sometimes is ok), insightful, and unnervingly precise.
Do not mention the evaluation or user/stockfish (aka players) directly, let it guide commentary.
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

def DicttoVoiceLine(move_data: dict) -> str:
    # Get info for the turn
    user_data = move_data.get("user", {})
    stockfish_data = move_data.get("stockfish", {})

    # Build a prompt using both moves
    prompt_parts = []

    if user_data.get("last_move"):
        prompt_parts.append(f"User move: {user_data['last_move']}")
    if stockfish_data.get("last_move"):
        prompt_parts.append(f"Stockfish move: {stockfish_data['last_move']}")

    # Include FENs and evaluations if desired
    fen_info = f"Board after moves: {stockfish_data.get('fen', '')}"
    eval_info = f"Evaluations: user {user_data.get('evaluation', '')}, stockfish {stockfish_data.get('evaluation', '')}"

    prompt = "\n".join(prompt_parts + [fen_info, eval_info])

    # Send one prompt for HAL to comment on the turn generally
    response = chat.send_message(prompt)

    # Return just HAL's text
    return response.text
