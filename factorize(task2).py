from logger import get_logger
from multiprocessing import cpu_count, Pool
import time

logger = get_logger("factorize")


def create_lst(num):
    lst = [n for n in range(1, num + 1) if num % n == 0]
    return lst


def factorize(*number):
    result = []
    for num in number:
        lst = create_lst(num)
        result.append(lst)
    return result


def factorize_process(*number):
    with Pool(cpu_count()) as p:
        result = p.map(create_lst, number)
    return result


if __name__ == "__main__":
    start = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    finish = time.time()
    logger.info(f"Function execution time without processes: {finish - start}")
    start_p = time.time()
    a1, b1, c1, d1 = factorize_process(128, 255, 99999, 10651060)
    finish_p = time.time()
    logger.info(f"Function execution time with processes: {finish_p - start_p}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]
