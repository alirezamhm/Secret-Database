from getpass import getpass
import hashlib
import sqlite3
import base64


hashed_psw = ''
psw = ''
try:
    with open('.password.txt', 'r') as pswfile: # read hashed value of the password from file
        hashed_psw = pswfile.read()
        psw =  getpass('Please enter your password: ') # get password without showing input in terminal
        while hashlib.md5(psw.encode('ASCII')).hexdigest() != hashed_psw:
            psw =  getpass("Wrong Password. Please Try again (press q to exit): ")
            if psw == 'q':
                break
except FileNotFoundError:
    with open('.password.txt', 'w+') as pswfile: # store the hash value of password in a file
        psw = getpass('Please create a password: ')
        pswfile.write(hashlib.md5(psw.encode('ASCII')).hexdigest()) 

if hashlib.md5(psw.encode('ASCII')).hexdigest() == hashed_psw:
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
        print('\n' + '*'*20)
        print('Commands: ')
        print('s: store a file')
        print('o: open a file')
        print('q: exit program')

        command = input('> ')
        
        if command == 'q':
            break
        elif command == 's':
            FILE_TYPES = {'txt', 'jpg', 'jpeg', 'png'}

            path = input('please enter the full path to your file (example: /home/alireza/pictures/sample.jpg) \n> ')
            try:
                full_name = path.split('/')[-1]
                name, extension = full_name.split('.')
                data = ''
                if extension not in FILE_TYPES:
                    print('Sorry this file type is not supported yet')
                    continue
            
                with open(path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode() # read data as byte and decode it to string to store
            except (ValueError, FileNotFoundError):
                print('This file does not exist')
                continue

            db_conn.execute('''INSERT INTO safe (FULL_NAME, NAME, EXTENSION, DATA)
                                VALUES ("{}", "{}", "{}", "{}");'''.format(full_name, name, extension, data))
            db_conn.commit()
        elif command == 'o':
            pass
        else:
            print("Invalid command")
    db_conn.close()