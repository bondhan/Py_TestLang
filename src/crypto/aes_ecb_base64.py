from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util import Padding


class AesEcbBase64():
    # mode = AES.MODE_CBC
    mode = AES.MODE_ECB
    bs = AES.block_size

    def __init__(self, hex_key):
        self.key = bytes.fromhex(hex_key)
        if (len(self.key) != 32):
            raise ValueError("Error key length, must be = 32 bytes")

        self.iv = self.key[8:self.bs+8]

    # encrypting
    def do_encrypt(self, plain):
        ciphered = Padding.pad(plain.encode('utf-8'), self.bs)
        if (self.mode is AES.MODE_CBC):
            self.cipher = AES.new(self.key, self.mode, self.iv)
        elif (self.mode is AES.MODE_ECB):
            self.cipher = AES.new(self.key, self.mode)

        ciphered = b64encode(self.cipher.encrypt(ciphered)).decode('utf-8')

        return ciphered

    # decrypting
    def do_decrypt(self, ciphered):

        encrypted = b64decode(ciphered.encode('utf-8'))
        if (self.mode is AES.MODE_CBC):
            self.cipher = AES.new(self.key, self.mode, self.iv)
        elif (self.mode is AES.MODE_ECB):
            self.cipher = AES.new(self.key, self.mode)

        plain = Padding.unpad(self.cipher.decrypt(encrypted), self.bs).decode('utf-8')

        return plain


debug = False
if (debug):
    thekey = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'

    aesecb = AesEcbBase64(thekey)
    ciphered = aesecb.do_encrypt("Secret Message")
    print("ciphered = " + ciphered)

    plain = aesecb.do_decrypt(ciphered)
    print("plain = " + plain)

    test = '9ge9OTesx/y3FMC70M3Met6pjTexMFDNPXOhhHiCJKYssIs30k6IhXIDkFf+FjITmr5/XjiMhsoX24xLZ3ADaMo3+Aev/jTdOG7d0kaMoDj1eCIuhzQE+ZlLbIaJRJi3ruRzqIx+aj9fsAnj2M8j2pbh0HjWtdThtfdNr+kTabRU3RuxnwESa0eKOl8YM9YMs9ufmmBlsAlSaajliAwo9o71/liqxxO+/fqwt1n631jxHEzjOf7sYEefFe1y1GMrZRHtzakype90l1ChlrE9jw=='
    plain = aesecb.do_decrypt(test)
    print("plain = " + plain)