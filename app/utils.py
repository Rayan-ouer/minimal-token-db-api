def extract_between(sentence: str, start: str, end: str) -> str:
    tokens: list[str] = sentence.split()
    res: list = []
    switch: bool = False

    for token in tokens:
        if token == start:
            switch = True
        if switch:
            res.append(token)
        if end in token:
            switch = False
    return " ".join(res)
