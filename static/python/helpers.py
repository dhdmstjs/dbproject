# -*- coding: utf-8 -*-
'''
Helper Functions for running sql queries from the main file
'''
#Following the tutorial of Andres Torres https://www.pythoncentral.io/hashing-strings-with-python/
import uuid
import hashlib
import datetime
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.md5(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return (password == hashlib.md5(salt.encode() + user_password.encode()).hexdigest())


def validate_args_exist(obj):
    for o in obj:
        if not o:
            return False
        
def today_date():
    return datetime.datetime.today().strftime('%Y-%m-%d')

def dates_to_array(date1, date2):
    labels = []
    data = []
    year1, month1 = [int(x) for x in date1[:7].split('-')]
    year2, month2 = [int(x) for x in date2[:7].split('-')]
    if [year1,month1] > [year2,month2]:
        month1, month2 = month2, month1
        year1, year2 = year2, year1
    if (year2 - year1 > 3):
        year2 = year1 + 3
    while (month1 <= month2  or year1 <= year2):
        labels.append(str(year1) +'-' + "%02d" % (month1))
        data.append(0)
        month1 += 1
        if month1 % 12 == 0:
            month1 = 0
            year1 +=1 
    return labels,data