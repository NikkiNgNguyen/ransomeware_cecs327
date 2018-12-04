#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption with HMAC Assignment

import os,sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes, hmac

BYTES = 16
BITS = 128
KEY_LENGTH = 32

def MyencryptMAC(message, EncKey, HMACKey):
    #make sure both keys are of the same length
    if len(EncKey) < KEY_LENGTH:
        raise ValueError("ERROR. The key has to be 32 bytes = 256 bits.")
        return
    #initialize IV
    iv = os.urandom(BYTES)
    #pad message: fill in extra space so it is the same
    #PKCS7: Public Key Cryptography Standards #7: used to sign and/or encrypt messages under a public key infrastructure
    padder = padding.PKCS7(BITS).padder() #BITS = 128, size of ciphertext
    padded_data = padder.update(message) #update(message) adds everything into the context
    padded_data += padder.finalize()
    #finalize() finishes the operation and obtains the remainder of the data
    '''encrypt with AES in CBC mode
    creates cipher instance, takes in algorithm, mode, and backend from Cipher library
    Backend implementations may provide a number of interfaces to support operations such as Symmetric encryption,
    Message digests (Hashing), and Hash-based message authentication codes (HMAC).'''
    cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend = default_backend())
    #creates Cipher(encrypt) object
    encryptor = cipher.encryptor()
    #encrypts the plaintext and generates associated ciphertext
    ct = encryptor.update(padded_data)
    h = hmac.HMAC(HMACKey, hashes.SHA256(), backend = default_backend())
    #takes in a message as bytes to hash and authenticate
    h.update(ct)
    #finalize the current context and return message digest as Bytes
    tag = h.finalize()
    #return ciphertext, iv, tag
    return ct, iv, tag

def MydecryptMAC(c, EncKey, HMACKey, iv, tag):
    #HMAC object takes a key and a HashAlgorithm instance. The key should be randomly generated bytes and is
    #recommended to be equal length to the digest size of the hash function chosen
    h = hmac.HMAC(HMACKey, hashes.SHA256(), backend = default_backend())
    #takes in a message as bytes to hash and authenticate
    h.update(c)
    #check that a given signature is correct. Will receive an exception if the signature is wrong
    h.verify(tag)
    #creates cipher instance, takes in algorithm, mode, and backend from Cipher library
    cipher = Cipher(algorithms.AES(EncKey), modes.CBC(iv), backend = default_backend())
    #creates decryptor object
    decryptor = cipher.decryptor()
    #decrypts the ciphertext
    p = decryptor.update(c)
    return p

def MyfileEncryptMAC(filepath):
    #Create 2 separate keys of the same length
    EncKey = os.urandom(KEY_LENGTH)
    HMACKey = os.urandom(KEY_LENGTH)
    #get file extension
    filename, extension = os.path.splitext(filepath)
    #with gets you better syntax and exceptions handling. Will automatically close the file
    #always ensures that a clean-up is used
    #rb = read binary
    # converts image to binary
    message = open(filepath,'rb') #refers to the imageFile object
    message = message.read()
    #encrypt and hash
    ct, iv, tag = MyencryptMAC(message, EncKey, HMACKey)
    #create new text file containing encryption in folder
    userFilepath = raw_input("please enter a save path for the encrypted file (Do not provide file name or extension): ")
    savepath = userFilepath + "/encrypted_HMAC_" + extension
    try:
        #create new file and write in binary mode
        newFile = open(savepath, 'wb')
        #write ciphertext to new file
        newFile.write(ct)
        #close file
        newFile.close()
    except Exception:
        print("invalid file path \n")
        userFilepath = raw_input("please enter a save path for the encrypted file (Do not provide file name or extension): ")
    #return ciphertext, iv, tag, encryption key, HMAC signature, file extension
    return ct, iv, tag, EncKey, HMACKey, extension

def MyfileDecryptMAC(ct, iv, EncKey, HMACKey, extension, tag):
    #decrypt ciphertext and verify the tag
    p = MydecryptMAC(ct, EncKey, HMACKey, iv, tag)
    #create new text file containing decryption in folder
    userFilepath = raw_input("please enter a save path for the decrypted file (Do not provide file name or extension): ")
    savepath = userFilepath + "/decrypted_HMAC_" + extension
    try:
        #create new file and write in binary mode
        newFile = open(savepath, 'wb')
        #write plaintext to new file
        newFile.write(p)
        #close file
        newFile.close()
    except Exception:
        print("invalid file path \n")
        userFilepath = raw_input("please enter a save path for the encrypted file (Do not provide file name or extension): ")
    return p

def menu():
    userInput = int(input("File Encryption w/ HMAC \n"
                          "1. Encrypt & Decrypt w/ HMAC on a ready file \n"
                          "2. Encrypt & Decrypt w/ HMAC on your own message \n"
                          "3. Exit \n"))
    return userInput

'''def main():
    key = os.urandom(KEY_LENGTH)
    while True:
        userInput = menu()
        #encrypt and decrypt a file in some directory
        if userInput == 1:
            thisFilepath = raw_input("enter an absolute file path: ")
            try:
                ct, iv, tag, EncKey, HMACKey, extension = MyfileEncryptMAC(thisFilepath)
                print("encryption ready")
                p = MyfileDecryptMAC(ct, iv, EncKey, HMACKey, extension, tag)
                print("decryption ready \n")
            except Exception:
                print("invalid file path \n")
        #create a message in a file and encrypt that message
        elif userInput == 2:
            thisFilepath = raw_input("enter an .txt file path: ")
            try:
                textfile = open(thisFilepath, 'w')
                fileMessage = raw_input("enter a message you want to encrypt: ")
                textfile.write(fileMessage)
                textfile.close()
                ct, iv, tag, EncKey, HMACKey, extension = MyfileEncryptMAC(thisFilepath)
                print("encryption ready \n")
                p = MyfileDecryptMAC(ct, iv, EncKey, HMACKey, extension, tag)
                print("decryption ready \n")
            except Exception:
                print("invalid file path \n")
        elif userInput == 3:
            raise SystemExit

main()'''


'''
Notes:
HMAC: calculate message authentication codes using a cryptographic hash function coupled with a secret key.
Verifies both the integrity and authenticity of a message. Double hashes: Hash(k2||Hash(k1||m))
HMAC object takes a key and a HashAlgorithm instance. The key should be randomly generated bytes and is
recommended to be equal length to the digest size of the hash function chosen
backend = a backend with methods for using cryptographic hash functions as method authentification codes
provides a number of interfaces to support operations such as Symmetric encryption, message digests(Hashing),
and Hash-based message authentification codes (HMAC)
SHA256() generates an almost unique 256-bit signature for a text (SHA-2 family)
message digest: a cryptographic has function containing a string of digits created by a one-way hashing formula
Backend implementations may provide a number of interfaces to support operations such as Symmetric encryption,
Message digests (Hashing), and Hash-based message authentication codes (HMAC).

Finalize(): after you call finalize(), you cannot use update(), copy(), verify(), and finalize() will raise an AlreadyFinalized exception
set it to a temp variable so that you can verify in MydecryptMAC()
copy() would work as well, it will create a new instance of HMAC that can be updated and finalized independently
'''
