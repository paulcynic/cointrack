from typing import List


def generate_follow_list(coins: List[str], currancies: List[str]):
    for coin in coins:
        for currancy in currancies:
            params = (coin, currancy)
            yield params
