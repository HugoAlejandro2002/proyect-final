import logging
import logging.handlers
import os
import colorlog

logs_directory = './logs'
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

class LoggerFactory:
    def __init__(self, logs_directory: str = logs_directory, retention_days: int = 14):
        self.logs_directory = logs_directory
        self.retention_days = retention_days
        self.console_handler = self._create_console_handler()
        self.file_handler = self._create_file_handler()

    def _create_console_handler(self) -> logging.Handler:
        """Creates a console handler with color formatting."""
        console_handler = colorlog.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s [%(levelname)s] [%(service)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(console_formatter)
        return console_handler

    def _create_file_handler(self) -> logging.Handler:
        """Creates a file handler with daily log rotation."""
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(self.logs_directory, 'application.log'),
            when='midnight',
            interval=1,
            backupCount=self.retention_days
        )
        file_handler.setFormatter(self._get_log_formatter())
        file_handler.suffix = "%Y-%m-%d"
        return file_handler

    def _get_log_formatter(self) -> logging.Formatter:
        """Defines the log format."""
        return logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(service)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def build_logger(self, service_name: str) -> logging.Logger:
        """
        Creates a logger specific to a service.
        :param service_name: Name of the service.
        :return: Configured logger.
        """
        logger = logging.getLogger(service_name)
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            logger.addHandler(self.console_handler)
            logger.addHandler(self.file_handler)

        def add_service_extra(record: logging.LogRecord) -> bool:
            record.service = service_name
            return True

        logger.addFilter(add_service_extra)
        return logger

logger_factory = LoggerFactory()


