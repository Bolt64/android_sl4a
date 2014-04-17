import android
import datetime
import time
import ConfigParser

droid=android.Android()

###################################################################################################################################
#
#     Some constants like path to store the generated files in and all

path_camera='/sdcard/'
timestamp=str(datetime.datetime.now().month)+str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)

config=ConfigParser.ConfigParser()
if config.read('/sdcard/charon_config.ini'):
	path_dict={}
	for section in config.sections():
		path_dict[section]=config.get(section,'path')
	for section in path_dict:
		if path_dict[section]=='default':
			path_dict[section]=path_dict['global']
	path_camera=path_dict['camera']

###################################################################################################################################
# Here's where you add other functions based on what you wanna do

def greeter(message):
    """
    This function just takes the message and echoes part of the meassge via sms
    """
	body=message['body'].split(' ',4)
	droid.smsSend(message['address'],'Hi '+body[3])

def camera_capture(message):
    """
    This function takes the message and clicks a picture after a delay
    or instantly if no delay is provided
    """
	delay=0
	body=message['body'].split(' ')
	try:
	if body[3].isdigit():
		delay=int(body[3])
	except IndexError:
		pass
	filename=timestamp+'.jpeg'
	time.sleep(delay)
	droid.cameraCapturePicture(path_camera+filename)

def speakmessage(message):
	body=message['body'].split(' ',3)[3]
	if not droid.ttsIsSpeaking().result:
		time.sleep(3)
		droid.ttsSpeak(body)

def getlocation(message):
    """
    This function takes the message and returns via sms the location of the phone
    """
	sender=message['address']
	if droid.locationProviderEnabled('gps').result:
		droid.startLocating(50000)
		time.sleep(155)
		location=droid.readLocation().result
		try:
			loc=location['gps']
		except KeyError:
			loc=location['network']
		lat=loc['latitude']
		lon=loc['longitude']
	else:
		droid.startLocating()
		time.sleep(15)
		location=droid.readLocation().result
		if location!={}:
			loc_network=location['network']
			lat=loc_network['latitude']
			lon=loc_network['longitude']
		elif location=={}:
			location=getLastKnownLocation().result
			loc_network=location['network']
			lat=loc_network['latitude']
			lon=loc_network['longitude']
	latlng='latitude:'+str(lat)+' longitude:'+str(lon)
	droid.smsSend(sender,latlng)


# A dictionary containing the functions. If you add any new functions be sure
# to add that function here
requests={'getlocation':getlocation,'speakmessage':speakmessage,'camera':camera_capture,'greeter':greeter}

####################################################################################################################################

# The necessary functions
# password_generator and the message_handler

def password_generator():
    """
    A simple password generator
    As of now, the generated password is just the sum of the month and the day
    """
	password=str(datetime.datetime.now().month+datetime.datetime.now().day)
	return password

password=password_generator()

def message_handler(message):
    body=message['body'].split(' ')
	if body[1]==password and body[2] in requests:
		requests[body[2]](message)

#####################################################################################################################################
#   Everything before this line describes the various functions
#	Everything after this line describes what will run.

messages=droid.smsGetMessages(True).result
message_queue=[]

for message in messages:
	if message['body'].startswith('python'):
		message_queue.append(message)
		droid.smsMarkMessageRead([message['_id']],True)

if message_queue:
	message_handler(message_queue[0])

#######################################################################################################################################
