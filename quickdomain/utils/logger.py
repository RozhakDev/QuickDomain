import logging
import os
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

def setup_logging(log_file: str):
    """
    Mengkonfigurasi logging untuk aplikasi.

    - Menggunakan RichHandler untuk output konsol yang indah.
    - Menggunakan RotatingFileHandler untuk menyimpan log ke file.

    :param log_file: Path ke file tempat log akan disimpan.
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            rich_tracebacks=True,
            log_time_format="[%Y-%m-%d %H:%M:%S]"
        )]
    )

    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    logging.getLogger().addHandler(file_handler)