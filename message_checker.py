"""
This is a continuously running script which checks for new messages every 2 seconds.
If there is any new message it starts the main script that is new_message_handler.py
"""

import android, time

droid=android.Android()

action="com.googlecode.android_scripting.action.LAUNCH_BACKGROUND_SCRIPT"
extras={"com.googlecode.android_scripting.extra.SCRIPT_PATH":"/sdcard/sl4a/scripts/new_message_handler.py"}     # Here's where the script you want to launch comes
clsname="com.googlecode.android_scripting"
pkgname="com.googlecode.android_scripting.activity.ScriptingLayerServiceLauncher"

myintent = droid.makeIntent(action,None,None,extras,None,clsname,pkgname).result

result0=droid.smsGetMessages(True).result
while True:
	result1=droid.smsGetMessages(True).result
	if len(result0)<len(result1):
		droid.startActivityIntent(myintent)
	result0=result1
	time.sleep(2)
