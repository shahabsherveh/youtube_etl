from _typeshed import WriteableBuffer
import json
from datetime import date
import logging


logger = logging.getLogger(__name__)


def load_path():
    file_path = f"./data/YT_data_{date.today()}.json"

    try:
        logger.info("Processing file: YT_data_{}.json".format(date.today()))

        with open(file_path, 'r', encoding='utf8') as file:
            data = json.load(file)

        return data
    except FileNotFoundError:
        logger.error("File not found:{}".format(file_path))
    except json.JSONDecodeError:
        logger.error("Invalid json file:{}".format(file_path))
