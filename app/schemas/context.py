from typing import TypedDict , List

class Context(TypedDict):
    question: str
    roles: List[str]