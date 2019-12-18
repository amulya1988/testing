import binascii

from Crypto.Cipher import AES
from py4j.java_gateway import JavaGateway, GatewayParameters

gateway = JavaGateway(
    gateway_parameters=GatewayParameters(address="tracker.thinktalentws48.click", auto_field=True))

bs = 16
key = "TheBestSecretKey"
cipher = AES.new(key, AES.MODE_ECB)


def encrypt_aes(text):
    raw = _pad(text)
    encrypted = cipher.encrypt(raw)
    encoded = binascii.hexlify(encrypted)
    return str(encoded, 'utf-8')


def decrypt_aes(encrypted):
    decoded = binascii.unhexlify(encrypted)
    decrypted = cipher.decrypt(decoded)
    return str(_unpad(decrypted), 'utf-8')


def decrypt_text(text):
    print(text)
    return gateway.entry_point.decryptText(text)


def encrypt_text(text):
    print(text)
    return gateway.entry_point.encryptText(text)


def encode_encrypt(text):
    print(text)
    return gateway.entry_point.encodeEncrypt(text)


def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]

# plaintext = 'ranjan'
# encrypted = encrypt_aes(plaintext)
# print('Encrypted: %s' % encrypted)
#
# # from java
# decrypted = decrypt_aes("A097D3B5C86933D582FF83AAA6EEC565")
# print('Decrypted: %s' % decrypted)
