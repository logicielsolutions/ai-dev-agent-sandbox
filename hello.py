"""Simple hello world module."""


def hello(name: str = "World") -> str:
    """Return a greeting message.
    
    Args:
        name: The name to greet.
        
    Returns:
        A formatted greeting string.
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b.
    """
    return a + b


if __name__ == "__main__":
    print(hello())
    print(f"2 + 3 = {add(2, 3)}")
