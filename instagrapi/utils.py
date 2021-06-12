import hashlib
import hmac
import json
import random
import string
import urllib

from . import config


class InstagramIdCodec:
    ENCODING_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    @staticmethod
    def encode(num, alphabet=ENCODING_CHARS):
        """Covert a numeric value to a shortcode."""
        num = int(num)
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            rem = num % base
            num //= base
            arr.append(alphabet[rem])
        arr.reverse()
        return "".join(arr)

    @staticmethod
    def decode(shortcode, alphabet=ENCODING_CHARS):
        """Covert a shortcode to a numeric value."""
        base = len(alphabet)
        strlen = len(shortcode)
        return sum(
            alphabet.index(char) * base ** (strlen - (idx + 1))
            for idx, char in enumerate(shortcode)
        )


def generate_signature_old(data):
    """Generate signature of POST data for Private API"""
    body = hmac.new(
        config.IG_SIG_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return "signed_body={body}.{data}&ig_sig_key_version={sig_key}".format(
        body=body,
        data=urllib.parse.quote(data),
        sig_key=config.SIG_KEY_VERSION,
    )


def generate_signature(data):
    return "signed_body=SIGNATURE.{data}".format(
        data=urllib.parse.quote_plus(data)
    )


def json_value(data, *args, default=None):
    cur = data
    for a in args:
        try:
            cur = cur[a] if isinstance(a, int) else cur.get(a)
        except (IndexError, KeyError, TypeError, AttributeError):
            return default
    return cur


def gen_password(size=10, symbols=False):
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    return "".join(random.choice(chars) for _ in range(size))


def gen_csrftoken(size=32):
    return gen_password(size, symbols=False)


def dumps(data):
    return json.dumps(data, separators=(",", ":"))


def generate_jazoest(symbols: str) -> str:
    amount = sum(ord(s) for s in symbols)
    return f'2{amount}'
