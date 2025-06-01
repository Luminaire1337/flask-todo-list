def friendly_string_sub(string: str, char_limit: int = 50) -> str:
    """
    Shorten a string to a friendly format with a maximum character limit.
    
    Args:
        string: The input string to be shortened.
        char_limit: The maximum number of characters allowed in the output string.
        
    Returns:
        A shortened version of the input string, ensuring it does not exceed the character limit.
    """
    if len(string) <= char_limit:
        return string
    return f"{string[:char_limit]}..."