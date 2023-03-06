import argparse
import os
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
from normalize import normalize
from logger import get_logger

logger = get_logger(__name__)

"""
--source [-s] test
"""

parser = argparse.ArgumentParser(description="Clear folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)

args = vars(parser.parse_args())

source = Path(args.get("source"))

folders = []


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_path = source / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / normalize(el.name))  # normalize the file name according to the standard
                logger.info(f"file named [{el.name}] has been moved to folder [{new_path.name}]")
                el.unlink()
            except OSError as error:
                logging.error(error)


def delete_empty_folder(path: Path) -> None:
    for dir in os.listdir(path):
        a = os.path.join(path, dir)
        if os.path.isdir(a):
            delete_empty_folder(a)
            if not os.listdir(a):
                logger.info(f"folder [{a}] has been deleted")
                os.rmdir(a)


if __name__ == "__main__":
    folders.append(source)
    grabs_folder(source)
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    delete_empty_folder(source)
