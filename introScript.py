from socket import *
import time

address= ( '10.0.0.15', 5000) #define server IP and port
client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
#client_socket.bind(('10.0.0.14', 5000))
#client_socket.settimeout(1) #Only wait 1 second for a response
sentNotification = 0
receiverEmail = 'chuguo14@gmail.com'
senderEmail = 'testingScripts@gmail.com'
subject = 'Trash is full'
message_text = 'Throw away trash ASAP'

while(1):
    print "looping" 
    data = "Trash?" #Set data request to Temperature
 
   #client_socket.sendto( data, address) #Send the data requet
 
    try:
        print "Currently Receiving" 
        rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
        # temp = float(rec_data) #Convert string rec_data to float temp
        print "Received data, send email" # Print the result
        if rec_data =="true":
                x = messages.create_message(senderEmail, receiverEmail, subject, message_text)
                messages.send(, , x)
                print 1
        else:
                print 2

 
    except:
        print "ERROR"
        pass
 
    time.sleep(2) #delay before sending next command



 
   # data = "Pressure" #Set data request to Pressure
 
    #client_socket.sendto( data, address) #Send the data request
 
   # try:
 
       # rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
       # Pressure = float(rec_data) #Convert string rec_data to float temp
       # print "Received data" # Print the result
 
    #except:
       # pass
 
    #time.sleep(2) #delay before sending next command
 
   # print ""
