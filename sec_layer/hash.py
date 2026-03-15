import os
import base64
import bcrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from abc import ABC, abstractmethod



class Hash(ABC):
    @abstractmethod
    def hash_input(self):
        pass
    @abstractmethod
    def verify_input(self):
        pass

    def make_kdf(self, password, salt = None, algorithm = None, iterations = 600000, key_length = 32) -> list:
        """ using PBKDF2 to generate derived key from something like user password to use it as KEK, DEK, and encryption key also
        algorithm must be form cryptography.hazmat.primitives.hashes algorithms
         it's returning pure derived key and base64 encoded derived key both in same return sentence"""
        if isinstance(password, str):
            password = password.encode("utf-8")
        if salt is None:
            salt = os.urandom(16)
        if algorithm is None:
            algorithm = hashes.SHA256()
        kdf = PBKDF2HMAC(
            algorithm=algorithm,
            salt=salt,
            iterations=iterations,
            length=key_length,
        )
        derived_key = kdf.derive(password)
        base64_derived_key = base64.urlsafe_b64encode(derived_key)
        return [salt, derived_key, base64_derived_key]



class Hash_bcrypt(Hash):
    """ small layer above bcrypt lib to make it easy to deal with it into this project (for me :) )"""

    def hash_input(self, data: str | bytes) -> bytes:
        """ it doesn't matter if you pass argument string or bytes, it will handel both of them and return final hashed output in bytes form """
        if isinstance(data, str):
            data = data.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(data, salt)


    def verify_input(self, data_entered: str | bytes, hashed_data: str | bytes) -> bool:
        """ it doesn't matter if you pass argument string or bytes, return True or False as result of matching """
        if isinstance(data_entered, str):
            data_entered = data_entered.encode("utf-8")
        if isinstance(hashed_data, str):
            hashed_data = hashed_data.encode("utf-8")
        return bcrypt.checkpw(data_entered, hashed_data)
