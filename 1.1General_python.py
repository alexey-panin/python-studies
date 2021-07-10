# Docstrings. Press 3 times " and then hit enter. Template should appear right away.

def test(a: int, b: str = None) -> str:
    """[summary]

    Args:
        a (int): [description]
        b (str, optional): [description]. Defaults to None.

    Returns:
        str: [description]
    """

    return f"{str(a)} {b}"


print(test(3, "hello"))
