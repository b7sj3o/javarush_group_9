from src.core import logger

def word_to_number(word: str) -> int:
    numbers_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    
    for k,v in numbers_map.items():
        if k in word:
            return v
    else:
        logger.error(f"Can't find rating for: '{word}'")
        return 0