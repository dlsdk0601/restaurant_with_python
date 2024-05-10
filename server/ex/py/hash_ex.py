from hashlib import sha3_512


def hash_password(base_salt: bytes, password: str) -> str:
    """sha 512 사용, base_salt 128bytes

    @param base_salt: 128bytes
    @param password: UTF-8 문자열

    >>> salt = bytes.fromhex('1234')
    >>> salt
    b'\\x124'
    >>> hash_password(salt, 'password')
    'a7e08224a964b30c6a0261cab08a94ab442af0462058b0fc738ac07c3b6773e5e3f4d5973f4db5762a296a68a3fe614dcaa8a289b8ad243816c57f9c6e3c00ab'
    """
    m = sha3_512()

    m.update(base_salt)
    m.update(password.encode('utf-8'))
    m.update(base_salt)

    return m.hexdigest()
