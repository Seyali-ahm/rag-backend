import re

def detect_repetition(text: str) -> bool:
    tokens = text.split()
    for i in range(len(tokens) - 1):
        if tokens[i] == tokens[i + 1]:
            return True
    return False

def detect_stammering(sentence: str, translation: str) -> bool:
    repeated = detect_repetition(translation)
    long_repeat = bool(re.search(r"(.+?)\1{2,}", translation))
    return repeated or long_repeat
