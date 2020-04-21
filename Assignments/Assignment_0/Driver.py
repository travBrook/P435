import subprocess
import sys
import time

host = "127.0.0.1"
port = 65431

#To run : >python driver.py
#Does NOT do anything with arguments... 
#I could not see a point to this...


'''
    Test one covers all the tests mentioned in the assignment.
    (1)In addition to the two initial STORE calls to the server in 
    alice.py, alice supplies two more STORE calls through arguments, and even 
    calls a GET. The test then sleeps for 5 seconds to ensure 
    that all of Alice's values get stored before bob starts.
    It will still work correctly if there is no sleep.
    (2)Bob runs three GET calls and one STORE. (3)In the bob.py file,
    one of the GET calls in messages tries to retrieve a key that is
    not stored in the server. 
'''

def test1():
    server = subprocess.Popen(['server.py'], shell=True)
    alice = subprocess.Popen(['alice.py', 'STORE joe=shmoe', 'STORE diggity=hehe', 'GET joe'], shell=True)

test1()
'''
    time.sleep(5)
    bob = subprocess.Popen(['bob.py', 'GET joe', 'Store blahby=hello'], shell=True)
    
print("TEST ONE START")
print()
test1()
time.sleep(10)
print("\nTEST ONE END")


print("\nSTARTING TEST TWO IN 3 seconds\n")
time.sleep(3)


'''
    #Testing of errroneous data
'''

def test2():
    alice = subprocess.Popen(['alice.py', 'Erroneous_Data', "No way this works?", "STORE bb="], shell=True)
    time.sleep(5)
    bob = subprocess.Popen(['bob.py', 'My', 'Name', 'IS BOB', 'GET bb', 'STORE michelle dd'], shell=True)

test2()
'''