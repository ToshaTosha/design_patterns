from src.utils.custom_exceptions import ArgumentTypeException
from enum import Enum

from src.core.event_type import event_type as EventType
from src.settings_manager import SettingsManager
from datetime import datetime
from src.core.abstract_logic import abstract_logic as AbstractLogic
from src.dto.observe_service import observe_service as ObserveService


class LogType(Enum):
    INFO = 1
    ERROR = 2
    DEBUG = 3


class Log:
    def __init__(self, log_type: LogType = LogType.INFO, message: str = ""):
        self.type = log_type
        self.message = message

    @property
    def type(self) -> LogType:
        return self._type

    @type.setter
    def type(self, value: LogType):
        if not isinstance(value, LogType):
            raise ArgumentTypeException('type', "LogType")
        self._type = value

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException('message', "str")
        self._message = value

    def __str__(self) -> str:
        return f"[{self.type.name}] {self.message}"

class logging(AbstractLogic):
    def __init__(self, settings: SettingsManager):
        self.min_type: LogType = settings.settings.min_log_type
        self.file_path: str = settings.settings.log_file_path
        self.log_to_console: bool = settings.settings.log_to_console
        self.log_to_file: bool = settings.settings.log_to_file
        ObserveService.append(self)

    def log(self, log: Log) -> None:
        log_str = self._format_log(log)
        if self.log_to_file:
            self._write_to_file(log_str)
        if self.log_to_console:
            print(log_str)

    def info(self, message: str) -> None:
        self.log(Log(LogType.INFO, message))

    def error(self, message: str) -> None:
        self.log(Log(LogType.ERROR, message))

    def debug(self, message: str) -> None:
        self.log(Log(LogType.DEBUG, message))

    def handle_event(self, event_type: EventType, params: str) -> None:
        if self._should_log(event_type):
            self.log(Log(event_type.log_type, params))

    def set_exception(self, ex: Exception) -> None:
        self._inner_set_exception(ex)

    def _format_log(self, log: Log) -> str:
        return f"{datetime.now().isoformat()}\t[{log.type.name}] {log.message}\n"

    def _write_to_file(self, log_str: str) -> None:
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(log_str)

    def _should_log(self, event_type: EventType) -> bool:
        return self.min_type.value >= event_type.log_type.value