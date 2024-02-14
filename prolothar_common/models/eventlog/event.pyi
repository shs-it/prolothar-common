class Event:
    activity_name: str
    attributes: dict[str,object]
    transition_id: str

    def __init__(self, activity_name, attributes: dict[str,object] = None, transition_id: str|None = None): ...
    def to_dict(self) -> dict: ...
