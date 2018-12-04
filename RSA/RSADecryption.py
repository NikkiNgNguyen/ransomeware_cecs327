#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption with HMAC Assignment

import os,sys #import only what you need
import json
from RSAEncryption import *
from generateKeys import generateKeys, checkKeys
from AESinCBCmodeHMAC import MydecryptMAC, MyfileDecryptMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import asymmetric

BYTES = 16
BITS = 128
KEY_LENGTH = 32
Y_OPT = ['y','Y']
N_OPT = ['n','N']

def MyRSADecrypt(RSACipher, C, IV, tag, ext, RSA_Privatekey_filepath):
    # initialize an RSA private_key encryption object and load pem privatekey from the RSA_privatekey_filepath
    with open(RSA_Privatekey_filepath, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), # PEM encoded key data
        password = None, # The password to use to decrypt the data. Should be None if the private key is not encrypted.
        backend = default_backend()) # an instance of PEMSerializationBackend

    key = private_key.decrypt(RSACipher, # ciphertext
        asymmetric.padding.OAEP(mgf = asymmetric.padding.MGF1( # OAEP padding, mgf - A mask generation function
        algorithm = hashes.SHA256()), # An instance of HashAlgorithm
        algorithm = hashes.SHA256(), # An instance of HashAlgorithm
        label = None)) # (bytes) A label to apply * This is a rarely used field and should typically be set to None or b"", which are equivalent *

    #Deconcatenate key back into 2 keys
    EncKey, HMACKey = key[:len(key)/2], key[len(key)/2:]

    #calls MyfileDecryptMAC and returns the plaintext message
    p = MyfileDecryptMAC(C, IV, EncKey, HMACKey, ext, tag)
    return p

def main():

    p = MyRSADecrypt(RSACipher, C, IV, tag, ext, RSA_Privatekey_filepath)

main()
