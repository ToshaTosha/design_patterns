import os
from datetime import datetime
from src.core.abstract_logic import abstract_logic
from src.dto.observe_service import observe_service
from src.settings import Settings as settings


class Logger(abstract_logic):
    LEVELS = {"INFO": 1, "WARNING": 2, "ERROR": 3, "DEBUG": 4}

    def __init__(self, settings: settings):
        super().__init__()
        observe_service.append(self)

        self.min_level = self.LEVELS[settings.min_log_level]
        self.log_to_file = settings.log_to_file
        self.log_file_path = settings.log_file_path if self.log_to_file else None

        if self.log_to_file:
            self._initialize_log_file()

    def _initialize_log_file(self):
        """Инициализирует файл логов, записывая время начала логирования."""
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(f"\n=== Logging started at {datetime.now().isoformat()} ===\n")

    def set_exception(self, exception: Exception):
        """Логирует информацию об исключении."""
        self._log("ERROR", f"Exception occurred: {exception}")

    def handle_event(self, event_type, params):
        """Обрабатывает события и логирует их в зависимости от уровня."""
        super().handle_event(event_type, params)

        message = params.get("message", "No message provided")
        if event_type.value in self.LEVELS:
            if self.LEVELS[event_type.value] >= self.min_level:
                self._log(event_type.value, f"Event: {event_type.value}, Message: {message}")

    def _log(self, level, message):
        """Формирует и записывает сообщение лога."""
        timestamp = datetime.now().isoformat()
        log_message = f"[{timestamp}] {level}: {message}"

        if self.log_to_file:
            self._write_to_file(log_message)
        else:
            print(log_message)

    def _write_to_file(self, log_message):
        """Записывает сообщение в файл логов."""
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(log_message + "\n")
