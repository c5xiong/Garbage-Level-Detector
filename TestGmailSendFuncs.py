from GmailSendFuncs import *

def main():
	print("Printing from main")
	printStuff()
	sendAndCreate()	 

#This if statement is crucial to runnning python stuff
#It is needed if you want to run the file directly
#__name__ is a a variable set by python interepreter
#to execute code in the function with __name__
if __name__ == '__main__':
	main()
