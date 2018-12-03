# Ransomware and Cryptography!
#### CECS 378 Nikki Nguyen & Jasmin Agustin


## TLS Server
### Step I: Setup your Node, Nginx server on a Ubuntu AWS instance
For this task, follow Setting up a Node Nginx server running on Ubuntu AWS (e.g., this tutorial). 
You can use whatever tech you want (any OS, any cloud provider like DigitalOcean, ....). Make sure you can SSH to your server.
Make sure you setup your github repo and can pull changes from your github repository onto your server.
Next, get a free domain (register with namecheap using your .edu email). 
In your DNS records, make sure your domain points to your aws instance. Make sure all is good and "It works".

### Step II: A simple HTTPS Server (separate deadline from the above step)
By now, you have a simple HTTP server that runs on either Nginx or Node.
Next, use "Let's Encrypt" to setup a free certificate (all instructions on Let's Encrypt). Test your TLS configuration with SSL Labs.  
Take a look at the "SSL Config" tutorials (SSL Config for Nginx as Reverse Proxy or SSL Config for Node).

### Links: 
[Ubuntu AWS Tutorial](https://blog.cloudboost.io/setting-up-an-https-sever-with-node-amazon-ec2-nginx-and-lets-encrypt-46f869159469?gi=b9499d469c98)<br />
[SSL Config for Nginx as Reverse Proxy](https://github.com/NikkiNgNguyen/ransomware_cecs378/blob/master/SSLNginxReverseProxy.md)<br />
[SSL Config for Node](https://github.com/NikkiNgNguyen/ransomware_cecs378/blob/master/SSLNode.md)<br />
[Let's Encrypt Tutorial](https://letsencrypt.org/docs/)<br />
[SSL Labs Test](https://www.ssllabs.com/ssltest/)


## File Encryption
In this phase, you'll develop modules that will encrypt/decrypt a file.
I recommend using [Python Cryptography](https://cryptography.io/en/latest/hazmat/primitives/) (hazmat ONLY!). If you decide to use JS, there is vanilla JS lib at [here](https://crypto.stanford.edu/sjcl/). Should you have any questions regarding the crypto building blocks then do not hesitate to ask the instructor.

### Step 1:
You will design these modules:
(C, IV)= Myencrypt(message, key):
In this method, you will generate a 16 Bytes IV, and encrypt the message using the key and IV in CBC mode (AES).  You return an error if the len(key) < 32 (i.e., the key has to be 32 bytes= 256 bits).
(C, IV, key, ext)= MyfileEncrypt (filepath):
In this method, you'll generate a 32Byte key. You open and read the file as a string. You then call the above method to encrypt your file using the key you generated. You return the cipher C, IV, key and the extension of the file (as a string).
You'll have to write the inverse of the above methods. 

### Step 2:
Modify your File Encryption to include the policy of Encrypt-then-[MAC](https://cryptography.io/en/latest/hazmat/primitives/mac/hmac/) for every encryption.
(C, IV, tag)= MyencryptMAC(message, EncKey, HMACKey)
(C, IV, tag, Enckey, HMACKey, ext)= MyfileEncryptMAC (filepath)
You will be asked to encrypt a JPEG file and then decrypt it and make sure you still can view the image.
You can use SHA256 in your HMAC.


## RSA File
In this project you will use and modify the module you developed previously (File Encryption). You'll also use the [OS package](https://docs.python.org/3/library/os.html) as well as [JSON package](https://docs.python.org/3/library/json.html).

### Step 1:
Next, you will a script that looks for a pair of RSA Public and private key (using a CONSTANT file path; PEM format). If the files do not exist (use OS package) then generate the RSA public and private key (2048 bits length) using the same constant file path.

### Step 2:
You are asked to write a method as below:
(RSACipher, C, IV, tag, ext)= MyRSAEncrypt(filepath, RSA_Publickey_filepath):
In this method, you first call MyfileEncryptMAC (filepath) which will return (C, IV, tag, Enckey, HMACKey, ext). You then will initialize an RSA public key encryption object and load pem publickey from the RSA_publickey_filepath. Lastly, you encrypt the key variable ("key"= EncKey+ HMACKey (concatenated)) using the RSA publickey in OAEP padding mode. The result will be RSACipher. You then return (RSACipher, C, IV, ext). Remember to do the inverse (MyRSADecrypt (RSACipher, C, IV, tag, ext, RSA_Privatekey_filepath)) which does the exactly inverse of the above and generate the decrypted file using your previous decryption methods.

### Step 3:
You can use the OS package to retrieve the current working directory. Then you can get a list of all files in this directory. For each file, encrypt them using MyRSAEncrypt from your new FileEncryptMAC module. Do this in a loop for all files (make sure you do not encrypt the RSA Private Key file). For every file that is encrypted, store the encrypted file as a JSON file. The attributes you have for each file are 'RSACipher', 'C', 'IV', 'tag' and 'ext'. The values are from MyRSAEncrypt method. Once the JSON fire is written (use json.dump() with file.write() methods) into a JSON file then you can remove the plaintext file (use os.remove() method). Note that you need to encode/decode your data before writing them into a JSON file.
Make sure then you can traverse thru all files within all sub-directories of a current working directory.  Encrypt all such files (either recursive execution or os.walk as an example).
Note: DO NOT test your script on any valuable file. It will be your responsibility if you lose any important data to you.

### Step 4:
Using [Pyinstaller](http://www.pyinstaller.org/) or [Py2exe](http://www.py2exe.org/) create an executable file from your step 3.
Do NOT run the executable file on important folders. Only test on a designated python working directory. You are responsible if you lose any important file.


##Public/Private Key to Server
After completing the previous labs, now you have a functioning payload.
Next you'll have your Python payload to communicate with your server.

Bonus Lab:
You setup a RESTful server on your AWS instance (take a look at "Quick Restful Node Server Setup" under [RESTful and JWT](https://github.com/NikkiNgNguyen/ransomware_cecs378/blob/master/RESTfulandJWT)). You want to make sure that your server has a simple DB with at least two API's. One is to POST a public/private key pair (stored in your MongoDB). The other is a GET request which contains a Public key in the hearder and it returns the corresponding private key in response.
After you deploy your RESTful server to your AWS, you modify your Python payload's keyGen method to POST the public/private keys to the server.
Write another Python script (name the executable as "MyUnlock.exe") that makes a GET request to retrieve the private key for the public key stored on the disk. It then stores the private key as a file. You can then add the decryption methods you developed previously to this script so it decrypts any encrypted file (stored as json) using the private key that it just received from your AWS server.
You may want to include an "App Key" in your requests. This is to authenticate the application to the server so your server does not respond to any connection coming from anywhere other than your own Python payload.


## Authors:
[Nikki Nguyen](https://github.com/NikkiNgNguyen)<br />
[Jasmin Agustin](https://github.com/JazzyJas0911)
