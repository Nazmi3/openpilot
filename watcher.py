# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


def debounce(wait_time):
    """
    Decorator that will debounce a function so that it is called after wait_time seconds
    If it is called multiple times, will wait for the last call to be debounced and run only this one.
    """

    def decorator(function):
        def debounced(*args, **kwargs):
            def call_function():
                debounced._timer = None
                return function(*args, **kwargs)
            # if we already have a call to the function currently waiting to be executed, reset the timer
            if debounced._timer is not None:
                debounced._timer.cancel()

            # after wait_time, call the function provided to the decorator with its arguments
            debounced._timer = threading.Timer(wait_time, call_function)
            debounced._timer.start()

        debounced._timer = None
        return debounced

    return decorator

class OnMyWatch:
	# Set the directory on watch
	watchDirectory = "./"

	def __init__(self):
		self.observer = Observer()

	def run(self):
		event_handler = Handler()
		self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
		self.observer.start()
		try:
			while True:
				time.sleep(5)
		except:
			self.observer.stop()
			print("Observer Stopped")

		self.observer.join()



import os
import signal
import subprocess

pro = None

@debounce(1)
def restart_debounched(s):
	print("restart")
	global pro
	if pro:
		pro.kill()
		print("program killed")
		pro = None
		start_openpilot()

def start_openpilot():
	print("start openpilot")
	global pro
	pro = subprocess.Popen('./selfdrive/manager/manager.py',stdout=subprocess.PIPE)

class Handler(FileSystemEventHandler):

	@staticmethod
	def on_any_event(event):
		global pro
		if event.is_directory:
			return None

		# elif event.event_type == 'created':
			# Event is created, you can process it now
			# print("Watchdog received created event - % s." % event.src_path)
		if event.event_type == 'modified':
			restart_debounched("should restart")
			
if __name__ == '__main__':
	start_openpilot()
	watch = OnMyWatch()
	watch.run()
	

# Importing required module
 
# Using system() method to
# execute shell commands

