import random
import string
from .models import ShortenedURL


def generate_short_code(length: int = 6) -> str:
    valid_chars: str = string.ascii_letters + string.digits

    while True:
        new_code: str = "".join(random.choices(valid_chars, k=length))

        if not ShortenedURL.query.filter_by(code=new_code).first():
            return new_code
