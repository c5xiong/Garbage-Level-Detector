from socket import *
import time

def runArduino(person):
    address= ( '10.0.0.15', 5000) #define server IP and port
    client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
    #client_socket.bind(('10.0.0.14', 5000))
    #client_socket.settimeout(1) #Only wait 1 second for a response
    sentNotification = 0
    receiver = person
    sender = 'testingScripts@gmail.com'
    subject = 'Trash is full'
    msg_txt = 'Throw away trash ASAP \n-Admin'
    msg_txt_html = "Throw away trash <b>ASAP</b>!! <br> -Admin"

    while(1):

        if curtime.tm_mday == person.finish.day || curtime.tm_mon != person.finish.month:
            break
        curtime = time.localtime(time.time())
        data = "Trash?" #Set data request to Temperature

        #client_socket.sendto( data, address) #Send the data requet
 
        try:
            rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
            # temp = float(rec_data) #Convert string rec_data to float temp
            if rec_data =="true":
                if curtime.tm_hour == 21 || curtime.tm_hour == 8:
                    SendMessage(sender, receiver, subject, msg_txt_html, msg_txt)
        except:
            pass
    
        time.sleep(2) #delay before sending next command

    return

