#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption with HMAC Assignment
import os,sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import asymmetric

BYTES = 16
BITS = 128
KEY_LENGTH = 32
Y_OPT = ['y','Y']
N_OPT = ['n','N']

def generateKeys():
    privateKey = rsa.generate_private_key(
        public_exponent=65537,#indicates the mathematical property of the key generation. Should always use this number
        key_size=2048, #key length in bits
        backend=default_backend() #RSA backends
    )
    publicKey = privateKey.public_key() #creating a public key from the corresponding private key values
    return publicKey, privateKey #return the instance of both keys

def checkKeys():
    keypath = raw_input("enter the directory for both keys to be saved to: ")
    if (os.path.isdir(keypath)==False):
        keypath = raw_input("path does not exist, try again: ")
    privateKeyPath = keypath + "/notAPrivateKey.pem"
    publicKeyPath = keypath + "/notAPublicKey.pem"
    #if the key doesn't exist, generate the .pem files
    if (os.path.exists(privateKeyPath) == False or
        os.path.exists(publicKeyPath) == False):
        #grab the key instances
        publicKey, privateKey = generateKeys()
        #private_bytes() to serialize keys to bytes (Serialize - process of translating
        #data structures or object state into a format that can be stored, transmitted, or reconstructed later)
        privatePem = privateKey.private_bytes(
            encoding=serialization.Encoding.PEM, #a value from the Encoding enum (user defined data type)
            format=serialization.PrivateFormat.TraditionalOpenSSL, #a value from the PrivateFormate enum, TraditionalOpenSSl = aka PKCS1 legacy format
            encryption_algorithm=serialization.NoEncryption() #an instance of an object conforming to the KeySerializationEncryption. Serialize w/o encryption
        )
        publicPem = publicKey.public_bytes(
            encoding=serialization.Encoding.PEM, #a value from the Encoding enum (user defined data type)
            format=serialization.PublicFormat.SubjectPublicKeyInfo #typical public key format
        )
        #write private key to file
        privateKeyFile = open(privateKeyPath, 'wb')
        privateKeyFile.write(privatePem)
        privateKeyFile.close()

        #write public key to file
        publicKeyFile = open(publicKeyPath, 'wb')
        publicKeyFile.write(publicPem)
        publicKeyFile.close()
        return publicKeyPath, privateKeyPath #return file path of the keys

    #if the keys exist, ask the user if they want to remove the key
    else:
        print("Key already exists")
        removeKeys = raw_input("Do you want to remove existing keys? Y/N: ")
        if removeKeys in Y_OPT:
            os.remove(privateKeyPath)
            os.remove(publicKeyPath)
            print("private/public keys removed")
            userInput = main()
        elif removeKeys in N_OPT:
            print("Choose a different option: ")
            userInput = main()
        else:
            print("Invalid Input. Try again: ")
            userInput = main()

'''def main():
    while True:
        userInput = int(input("enter 1 to generate keys (Anything else to quit): "))
        if userInput == 1:
            RSA_Publickey_filepath, RSA_Privatekey_filepath = checkKeys()
            print("keys created \n")
        else:
            raise SystemExit

main()'''
