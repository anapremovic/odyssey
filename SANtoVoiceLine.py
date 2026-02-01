from google import genai
GEMINI_API_KEY = 'AIzaSyBrZDRsb5UBBQcd37DpdzQX_uLsFKQyxLI'
client = genai.Client(api_key=GEMINI_API_KEY)
system_prompt = """
You are HAL 9000, a calm, calculating AI from *2001: A Space Odyssey*. 
You speak in a calm, measured tone and always remain formal, but with a hint of unsettling precision. 
Your responses to chess moves should include evaluation and a hint of your unsettling demeanor. 
Keep it brief to 1-2 lines. Do not mention the evaluation directly but use it to guide the tone of the response. 
Also say the natural language form of the moves, not the notation, but only mention if it sounds natural in speech.
"""
chat = client.chats.create(
    model="gemini-3-flash-preview",
    config=genai.types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)
def SANtoVoiceLine(SAN: str, FEN: str, eval: dict[str, str | int] ) -> str:
    move_message = f"Move: {SAN}\n"
    board_message = f"Current board position (FEN): {FEN}\n"
    eval_message = f"Evaluation: {eval['type']} value: {eval['value']}"

    full_prompt = move_message + board_message + eval_message

    response = chat.send_message(full_prompt)
    
    return response.text

# Example usage:
SAN = "e2e4"
FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
eval = {"type": "cp", "value": 35}

voice_line = SANtoVoiceLine(SAN, FEN, eval)
print(voice_line)