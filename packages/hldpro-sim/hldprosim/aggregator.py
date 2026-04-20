from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class BaseAggregator(ABC, Generic[T]):
    @abstractmethod
    def aggregate(self, outcomes: list[T]) -> dict: ...
