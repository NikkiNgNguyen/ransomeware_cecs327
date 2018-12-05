#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption with HMAC Assignment

import os, sys, json, base64, subprocess
from generateKeys import generateKeys, checkKeys, getKeys
from RSAEncryption import MyRSAEncrypt
from RSADecryption import MyRSADecrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import asymmetric

def repositoryWalk():
    newdir = raw_input("enter a project directory to disinfect: ")

    os.chdir(newdir)
    print("current directory: " + os.getcwd())
    #RSA_Publickey_filepath, RSA_Privatekey_filepath = checkKeys()
    for root, dirs, files in os.walk(newdir):
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        for d in dirs:
            print (os.path.relpath(os.path.join(root, d), "."))
        for f in files:
            ff = (os.path.relpath(os.path.join(root, f), "."))
            if f.endswith(('.json')):
                print(f)
                with open(f, 'r') as myFile:
                    jsonFile = myFile.read()
                    data = json.loads(jsonFile)

                    RSACipher = base64.b64decode(data['RSACipher'].encode('ascii'))
                    ct = base64.b64decode(data['ct'].encode('ascii'))
                    iv = base64.b64decode(data['iv'].encode('ascii'))
                    tag = base64.b64decode(data['tag'].encode('ascii'))
                    extension = base64.b64decode(data['extension'].encode('ascii'))
                    RSA_Publickey_filepath, RSA_Privatekey_filepath = checkKeys()
                    p = MyRSADecrypt(RSACipher, ct, iv, tag, extension, RSA_Privatekey_filepath)


                    filename,ext = os.path.splitext(f)
                    decryptedFile = os.path.join(root + filename + "_decrypted_" + extension)

                    privateKeyFile = open(decryptedFile, 'wb')
                    privateKeyFile.write(p)
                    privateKeyFile.close()

                if ff.endswith('.json'):
                    os.remove(ff)


repositoryWalk()
