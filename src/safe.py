from getpass import getpass
import hashlib
import sqlite3

hashed_psw = ''
psw = ''
try:
    with open('.password.txt', 'r') as pswfile:
        hashed_psw = pswfile.read()
        psw =  getpass('Please enter your password: ')
        while hashlib.md5(psw.encode('ASCII')).hexdigest() != hashed_psw:
            psw =  getpass("Wrong Password. Please Try again (press q to exit): ")
            if psw == 'q':
                break
except FileNotFoundError:
    with open('.password.txt', 'w+') as pswfile:
        psw = getpass('Please create a password: ')
        pswfile.write(hashlib.md5(psw.encode('ASCII')).hexdigest()) 

if hashlib.md5(psw.encode('ASCII')).hexdigest() == hashed_psw:
    print('in')
    db_conn = sqlite3.connect('safe.db')
    try:
        db_conn.execute('''CREATE TABLE safe (
                            full_name TEXT NOT NULL PRIMARY KEY,
                            name TEXT NOT NULL,
                            extension TEXT NOT NULL,
                            data TEXT NOT NULL);''')
        print("Your safe has been created")
    except sqlite3.OperationalError:
        print("You are connected to your safe")
    while True:
        print('*'*20)
        print('Commands: ')
        print('s: store a file')
        print('o: open a file')
        print('q: exit program')

        command = input('> ')
        
        if command == 'q':
            break
        elif command == 's':
            pass
        elif command == 'o':
            pass
        else:
            print("Invalid command")