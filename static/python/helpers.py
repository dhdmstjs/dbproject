# -*- coding: utf-8 -*-
'''
Helper Functions for running sql queries from the main file
'''
#Following the tutorial of Andres Torres https://www.pythoncentral.io/hashing-strings-with-python/
import uuid
import hashlib
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.md5(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return (password == hashlib.md5(salt.encode() + user_password.encode()).hexdigest())

