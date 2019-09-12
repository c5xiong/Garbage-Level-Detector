Garbage Detector Project

Summary:
This project is designed to detect the amount of trash in a trash can and notify the person responsible for throwing out the trash.
The hardware that is used to detect if the trash can is full or not is an Arduino microprocessor with a laser. When the trash level
reaches the max amount, the Arduino with a W51000 Ethernet shield will send a signal to the Python Flask Server that is running on
a Raspberry Pi. After that, the server will send a gmail to the one responsible for throwing out the trash. The settings of the server
is easily adjustable via a webapp. 
