"""
Shared Memory
Acts as a common storage for all agents.
"""

from typing import Any
from rich import print


class SharedMemory:
    """
    Shared memory accessible by all agents.
    """

    def __init__(self) -> None:
        self._memory: dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:
        """
        Store data in shared memory under the given key.

        Args:
            key (str): Unique key identifier.
            value (Any): Data value to store.
        """
        self._memory[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve data from shared memory by key.

        Args:
            key (str): Key to look up.
            default (Any, optional): Fallback value if key is not found. Defaults to None.

        Returns:
            Any: Stored value or default if key doesn't exist.
        """
        return self._memory.get(key, default)

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in shared memory.

        Args:
            key (str): Key to verify.

        Returns:
            bool: True if key exists, False otherwise.
        """
        return key in self._memory

    def clear(self) -> None:
        """
        Clear all stored memory.
        """
        self._memory.clear()

    def display(self) -> None:
        """
        Print formatted contents of current memory using Rich.
        """
        print(f"[bold cyan]{'=' * 60}[/bold cyan]")
        if not self._memory:
            print("[italic yellow]Shared memory is currently empty.[/italic yellow]")
        else:
            for key, value in self._memory.items():
                print(f"[bold green]{key}:[/bold green] {value}")
        print(f"[bold cyan]{'=' * 60}[/bold cyan]\n")
