from typing import Iterable


class OutputUtil:
    """
    Utility class to write iterables
    """
    @staticmethod
    def write_new_line_to_console(strs: Iterable[str]) -> None:
        """
        Writes each item of iterable to new line to console.

        :param strs:
        :return None:
        """
        for value in strs:
            print(value)
