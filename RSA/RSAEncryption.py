#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption with HMAC Assignment

import os, sys
import json
from generateKeys import generateKeys, checkKeys
from AESinCBCmodeHMAC import MyencryptMAC, MyfileEncryptMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import asymmetric

Y_OPT = ['y','Y']
N_OPT = ['n','N']

def MyRSAEncrypt(filepath,RSA_Publickey_filepath):
    #backend = default_backend()
    #call MyfileEncryptMAC
    ct, iv, tag, EncKey, HMACKey, extension = MyfileEncryptMAC(filepath)
    #initialize an RSA public_key encryption object and load pem publickey from the RSA_publickey_filepath
    with open(RSA_Publickey_filepath, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), #PEM encoded key data
        backend = default_backend()) #an instance of PEMSerializationBackend
    RSACipher = public_key.encrypt(EncKey + HMACKey, # message - "key" = EncKey + HMACKey (concatenate)
        asymmetric.padding.OAEP(mgf = asymmetric.padding.MGF1( # OAEP padding, mgf - A mask generation function, takes a hash algorithm
        algorithm = hashes.SHA256()), # An instance of HashAlgorithm
        algorithm = hashes.SHA256(), # An instance of HashAlgorithm
        label = None)) # (bytes) A label to apply * This is a rarely used field and should typically be set to None or b"", which are equivalent *
    return RSACipher, ct, iv, tag, extension

def menu():
    userInput = int(input("RSA Menu \n"
                          "1. RSA Encrypt a text file \n"
                          "2. RSA Encrypt a ready file \n"
                          "3. Exit \n"))
    return userInput

def main():
    while True:
        userInput = menu()
        if userInput == 1:
            thisFilepath = raw_input("enter an absolute file path: ")
            try:
                newTxtFile = open(thisFilepath, 'wb')
                fileMess = raw_input("enter a message: ")
                newTxtFile.write(fileMess)
                newTxtFile.close()
                RSA_Publickey_filepath, RSA_Privatekey_filepath = checkKeys()
                RSACipher, ct, iv, tag, extension = MyRSAEncrypt(thisFilepath, RSA_Publickey_filepath)
                print("encryption complete")
            except Exception:
                print("invalid file path \n")
        elif userInput == 2:
            thisFilepath = raw_input("enter an absolute file path: ")
            try:
                RSA_Publickey_filepath, RSA_Privatekey_filepath = checkKeys()
                RSACipher, ct, iv, tag, extension = MyRSAEncrypt(thisFilepath, RSA_Publickey_filepath)
                print("encryption complete")
            except Exception:
                print("invalid file path \n")
        elif userInput == 3:
            raise SystemExit

    print("done")



#main()
