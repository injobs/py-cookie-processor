from abc import abstractmethod
from typing import Generator


class AbstractDatasource:
    """
    Abstract datasource class that all other datasource should implement
    """

    def __init__(self, **kwargs):
        self._ignore_error = kwargs.get('ignore_error') or True

    @abstractmethod
    def validate(self):
        """
        Validate data source

        :raise:
            ProgramError: When the datasource is malformed or missing or inaccessible.
        """
        raise NotImplementedError

    @abstractmethod
    def get_rows(self) -> Generator[dict, None, None]:
        """
        :return:
            Generator[dict]: In {'cookie': <VALUE:str>, 'timestamp': <VALUE:datetime>}
        """
        raise NotImplementedError
