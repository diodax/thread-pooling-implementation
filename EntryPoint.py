from Utils import profile
from concurrent.futures import ThreadPoolExecutor
import math

PRIMES = [
    1099726899285419,
    1099726899285419,
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]


def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


@profile
def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))


@profile
def main2():
    for number in PRIMES:
        is_prime(number)


if __name__ == '__main__':
    main()
    main2()
