from typing import List


def generate_follow_list(coins: List[str], currancies: List[str]):
    for coin in coins:
        for currancy in currancies:
            params = (coin, currancy)
            yield params


def validate_phone(raw_phone: str) -> str:
    num = "".join(filter(str.isdigit, raw_phone))
    if len(num) < 10 or len(num) > 11 or num[-10] != '9':
        return num
    phone = "8 (9{}{}) {}{}{}-{}{}-{}{}".format(*num[-9:])
    return phone
