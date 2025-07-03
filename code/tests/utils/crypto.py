import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_numbers = public_key.public_numbers()
    n = base64url_encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, "big"))
    e = base64url_encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, "big"))

    kid = "02B1174234C29F8EFB69911438F597FF3FFEE6B7"

    jwks = {
        "keys": [
            {
                "kty": "RSA",
                "n": n,
                "e": e,
                "alg": "RS256",
                "use": "sig",
                "kid": kid,
            }
        ]
    }

    return private_pem, jwks, kid
