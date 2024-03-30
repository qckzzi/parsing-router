from typing import Final


class Error(Exception):
    def __init__(self, description: str) -> None:
        self.description: Final[str] = description
        super().__init__(description)


class QueueNotMatchError(Error):
    def __init__(self, not_matched_queue: str) -> None:
        super().__init__(f"Queue '{not_matched_queue}' doesn't match")


class EntityTypeNotMatchError(Error):
    def __init__(self, not_matched_entity_type: str) -> None:
        super().__init__(f"Entity type '{not_matched_entity_type}' doesn't match")
