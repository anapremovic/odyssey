import sys
from typing import Optional

pieceDict = {
    'knight':'N',
    'king': 'K',
    'queen': 'Q',
    'rook': 'R',
    'bishop': 'B',
    'pawn': ''}

captureDict = {
    'capture': 'x', 'captures': 'x',
    'take': 'x', 'takes': 'x'
}

castlingDict = {
    'kingside': '0-0', 'king-side': '0-0',
    'short': '0-0',
    'queenside': '0-0-0', 'queen-side': '0-0-0',
    'long': '0-0-0'
}

checkDict = {
    'check': '+',
    'checkmate': '#', 'mate': '#'
    }

validFiles = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
validRanks = {'1', '2', '3', '4', '5', '6', '7', '8'}

phoneticFiles = {
    'alpha': 'a', 'alfa': 'a', 'aye': 'a', 'ay': 'a',
    'brava': 'b', 'bee': 'b',
    'charlie': 'c', 'charley': 'c', 'see': 'c', 'sea': 'c', 
    'delta': 'd', 'dee': 'd',
    'echo': 'e', 'ee': 'e',
    'foxtrot': 'f', 'eff': 'f',
    'golf': 'g', 'gee': 'g',
    'hotel': 'h', 'aitch': 'h',
}

phoneticRanks = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
}

def clean(text: str) -> list[str]:
    return text.lower().strip().split()

def detectPiece(words: list[str]) -> str:
    for word in words:
        if word in pieceDict:
            return pieceDict[word]
    return ''

def detectSquare(words: list[str]) -> Optional[str]:

    import re 

    text = ' '.join(words)

    match = re.search(r'([a-h])([1-8])', text)
    if match:
        return match.group(1) + match.group(2)

    file = ''
    rank = ''

    for word in words:
        # normalize token (strip punctuation)
        token = re.sub(r'[^a-z0-9]', '', word.lower())
        if token in phoneticFiles and not file:
            file = phoneticFiles[token]
        elif token in phoneticRanks and not rank:
            rank = phoneticRanks[token]
        # also accept direct single-letter files like 'a'..'h'
        elif token in validFiles and not file:
            file = token
        # and direct numeric ranks like '1'..'8'
        elif token in validRanks and not rank:
            rank = token

    
    if file and rank:
        return file + rank
    return None 

def detectCapture(words: list[str]) -> str:
    for word in words:
        if word in captureDict:
            return captureDict[word]
    return ""

def detectCheck(words: list[str]) -> str:
    for word in words:
        if word in checkDict:
            return checkDict[word]
    return ""

def detectSourceAndDestination(text: str) -> Optional[tuple[str,str]]:
    import re

    # Pattern 1: "e4 to e5" or "e4-e5"
    pattern1 = r'([a-h][1-8])\s*(?:to|-)\s*([a-h][1-8])'
    match = re.search(pattern1, text.lower())
    if match:
        return (match.group(1), match.group(2))
    
    # Pattern 2: "e4 e5" (two squares with space)
    pattern2 = r'\b([a-h][1-8])\s+([a-h][1-8])\b'
    match = re.search(pattern2, text.lower())
    if match:
        return (match.group(1), match.group(2))
    
    return None

def parse(text: str) -> str | None:

    words = clean(text)

    for word in words:
        if word in castlingDict:
            return castlingDict[word]
        
    source_dest = detectSourceAndDestination(text)
    if source_dest:
        source, dest = source_dest
        uci = source + dest
        return uci

    piece = detectPiece(words)
    square = detectSquare(words)
    capture = detectCapture(words)
    check = detectCheck(words)

    if not square:
        return None
    
    san = piece + capture + square + check

    return san

if __name__ == "__main__":
    if len(sys.argv) > 1:
        move_text = " ".join(sys.argv[1:])
        san = parse(move_text)
        print(san)
    else:
        print("Please provide a move in natural language.")

