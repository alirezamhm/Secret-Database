from getpass import getpass
import hashlib


hashed_psw = ''
psw = ''
try:
    with open('.password.txt', 'r') as pswfile:
        hashed_psw = pswfile.read()
        psw =  getpass('Please enter your password: ')
        while hashlib.md5(psw.encode('ASCII')).hexdigest() != hashed_psw:
            psw =  getpass("Wrong Password. Please Try again: ")
            if psw == 'q':
                break
    if hashlib.md5(psw.encode('ASCII')).hexdigest() == hashed_psw:
        print('got in')
except FileNotFoundError:
    with open('.password.txt', 'w+') as pswfile:
        psw = getpass('Please create a password: ')
        pswfile.write(hashlib.md5(psw.encode('ASCII')).hexdigest()) 