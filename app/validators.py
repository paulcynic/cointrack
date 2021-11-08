import hmac
import hashlib
import base64
from typing import Optional
from app.user_data import USERS


SECRET_KEY = "672b65de9006fa8d1687b39d85eba84c9decdbc8663381884c9722be151c1a2b"
PASSWORD_SALT = "9cdc7437bc56ba94397067033b60b260593a72ef8cc2b2d47909c42425aaa310"


def sign_data(data: str) -> str:
    return hmac.new(
            SECRET_KEY.encode(),
            msg=data.encode(),
            digestmod=hashlib.sha256
            ).hexdigest().upper()


def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    # сравнивает переданную через куки подпись и реальную подпись
    if hmac.compare_digest(valid_sign, sign):
        return username


def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash = USERS[username]["password"].lower()
    return password_hash == stored_password_hash


def create_user_cookie(username) -> str:
    username_signed = base64.b64encode(username.encode()).decode() + "." + sign_data(username)
    return username_signed


def validate_phone(raw_phone: str) -> str:
    num = "".join(filter(str.isdigit, raw_phone))
    if len(num) < 10 or len(num) > 11 or num[-10] != '9':
        return num
    phone = "8 (9{}{}) {}{}{}-{}{}-{}{}".format(*num[-9:])
    return phone

