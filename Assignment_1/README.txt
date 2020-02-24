For initialization and running map reduce, you can find example 
commands in MapRedDataSets/commands.txt 
PLEASE RUN THE COMMANDS FROM THE ASSIGNMENT ONE DIRECTORY

Right now, the only local communication that happens is when the
init.py file in the master directory spawns the mapper and reducer 
main processes... I have not implemented it yet, -- although there
is remnants of the code lying around -- but for the future, the
idea would be that you spawn servers for the mappers/reducers,
and make a remote procedure call on the servers to run the main.py
files. This was left to the end because it is easier to test without
having to start these mapper/reducer servers before each initialization.

It is not yet possible to run map reduce on a real distributed system, 
but the opportunity has been left open. 

As of now, the only text file it works with is the aSimpleText.txt file.
The other txt files have characters that mess with the google protocol buffers. 

If you get an error like below, you just need to wait about 30 seconds before you try again.

Traceback (most recent call last):
  File "C:\Users\travb\Desktop\P435\Assignment_1\Master\init.py", line 163, in <module>
    except psutil.AccessDenied:  # JUST WAIT
NameError: name 'psutil' is not defined

The lines that make this error occur usualluy just unbind the ports
that we use. Without first unbinding, the program will fail hard. 
Yes its annoying, but at least you dont have to manually kill off the processes

