from cryptography.fernet import Fernet
from abc import ABC, abstractmethod

class Encrypt(ABC):
    """ base class for encryption and decryption """
    @abstractmethod
    def encrypt(self, data):
        pass
    @abstractmethod
    def decrypt(self, data):
        pass


class FernetEncrypt(Encrypt):
    """ using Fernet encryption """
    def __init__(self, key):
        self.fernet = Fernet(key)
    @classmethod
    def set_key(cls, key):
        return cls(key)
    def encrypt(self, data) -> bytes:
        """ data can be any string or bytes """
        if isinstance(data, str):
            data = data.encode("utf-8")
        return self.fernet.encrypt(data)

    def decrypt(self, encrypted_data) -> bytes:
        """ data can be any string or bytes """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode("utf-8")
        return self.fernet.decrypt(encrypted_data)