class token():
    def __init__(self, _type: str, lit: str) -> None:
        self.type: str = _type
        self.lit: str = lit

    def __str__(self) -> str:
        return self.type + ': ' + self.lit

    def __eq__(self, value: str) -> bool: # type: ignore
        if self.lit == value:
            return True
        return False
    
    def __ne__(self, value: str) -> bool: # type: ignore
        if self.lit != value:
            return True
        return False
    
    def __contains__(self, value):
        return self.lit in value