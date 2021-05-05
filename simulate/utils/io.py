import json

from log import logger


def json_dump(data: any, file_path: str):
    json.dump(data, open(file_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    logger.info("dumped content to file_path: " + file_path)


def json_load(file_path: str):
    return json.load(open(file_path, "r", encoding="utf-8"))