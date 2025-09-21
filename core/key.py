from hashlib import pbkdf2_hmac
import os

password = b"my_secure_password"
salt = os.urandom(16)
iterations = 100000

key = pbkdf2_hmac('sha256', password, salt, iterations, 32)
print(key.hex())