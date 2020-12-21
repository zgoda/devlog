from typing import Union

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding, NoEncryption, PrivateFormat, PublicFormat,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'])


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_password_hash(secret: str, password: str) -> bool:
    return pwd_context.verify(password, secret)


def generate_private_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def serialize_private_key(
            key: rsa.RSAPrivateKeyWithSerialization, decode: bool = True
        ) -> Union[bytes, str]:
    binary = key.private_bytes(
        encoding=Encoding.PEM, format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    if decode:
        return binary.decode('utf-8')
    return binary


def generate_public_key(private_key: rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
    return private_key.public_key()


def serialize_public_key(
            key: rsa.RSAPublicKeyWithSerialization, decode: bool = True
        ) -> Union[bytes, str]:
    binary = key.public_bytes(
        encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
    )
    if decode:
        return binary.decode('utf-8')
    return binary
