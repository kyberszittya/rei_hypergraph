import hashlib
import abc


class InterfaceIdentifierGenerator(type):
    """
    Interface identifier generator
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'generate_id') and
                callable(cls.generate_id) or
                NotImplemented)

    @abc.abstractmethod
    def generate_id(self, ident: str, timestamp: int) -> bytes:
        """
        Generate an ID based on timestamp and/or string

        :param ident: identification string to be encoded
        :param timestamp: timestamp of generation ()
        :return: the identification as a bytestream
        """
        raise NotImplementedError


class IdentifierGeneratorSha224(metaclass=InterfaceIdentifierGenerator):
    """
    Identifier generator based on a prefix and name
    """

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.hash_generator = None

    def generate_id(self, ident: str, timestamp: int) -> bytes:
        """
        Generate a brand new identification based on a string input to a bytestream
        The ID generation is based on the SHA3-224 algorithm.

        Encoding:
        encoding:= ident + timestamp

        :param ident: the identification string to be encoded into bytestream
        :param timestamp: the timestamp of id generation (used in identification process)
        :return: bytestream
        """
        self.hash_generator = hashlib.new('sha3_224')
        self.hash_generator.update(':'.join([
            self.prefix, ident, str(timestamp)]).encode('utf8'))
        return self.hash_generator.digest()
