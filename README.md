android_sl4a
============

So here's how the whole thing works.

First, you start message_checker.py. It checks every 2 seconds if there's any
new message and if so, starts new_message_handler.py.

Now, the actual program starts its magic. new_message_handler (nmh) checks the
inbox for any messages starting with the keyword "python". If so, it adds that
message to the message queue. Next, if the message queue is non empty, the
message_handler function is run on the first member of the queue. This function
checks that the message starts with the valid keyword "python" and contains a
valid password. The rest of the message mentions the function to be executed
and its parameters. The mentioned function is then run. These functions take
only a single argument that is the SMSmessage object. So if you want to add any
of your own functions, make sure they follow the API and add them to the
requests dictionary. 
