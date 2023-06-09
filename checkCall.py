import time
import serial
import os
import subprocess
import datetime

# DateTime for log
now = datetime.datetime.now()

# Declare the device address
serialDevice = "/dev/ttyACM0"

# Target phone number fater validation
targetPhoneNumber = "555555555"

# Open phone device, baudrate and connection timeout
# Some devices are a little slow getting the initial connection
# So we declare 5s for timeout
phone = serial.Serial(serialDevice,  19200, timeout=5)

# Try catch function
try:
    time.sleep(1)

    # Waiting for voice call loop
    while(1):
        # Get phone responses
        x = phone.readline()

        # Debug, printing phone responses
        # print(x)

        # If we get active connection line with RING response, do the job
        # NOTES: 
        # 1. Some old GSM Modems doesn't have RING response.
        # 2. If this is the case, we need to loop AT+CLCC to check if there is a active Caller_ID 
        if (x == b'RING\r\n'):
            # Connection line is active
            # Log the ring event
            print('Ringing - Someone is calling')
            
            # Lets RING one more time on the original traffic subject
            time.sleep(5)
            
            # Log connection date/time
            print("Connection Date/Time: ", now)

            # Run atcom AT commands
            proc = subprocess.Popen(["atcom --port " + str(serialDevice) + " -b 19200 AT+CLCC"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            
            # Log the command object output 
            print("CID Output: ", out)
            
            # Convert output object to string so we can use it later
            word =  str(out)
            
            # Hangup the call 
            os.system("atcom --port " + str(serialDevice) + " -b 19200 AT+CHUP >/dev/null 2>&1")

            # Clear the Caller ID string for unwanted chars 
            new_string = word.replace('\r\n','')
            
            # All done ... Lets check the permited numbers file
            with open('numbers_permited.txt') as f:
                while True:
                    line = f.readline()
                    if line.strip():
                        if new_string.find(line.strip()) != -1:
                            # Log the event if caller id found
                            print("Caller ID Found", line.strip())
                            os.system('atcom --port ' + str(serialDevice) + ' -b 115200 ATDT"' + str(targetPhoneNumber) + ';" >/dev/null 2>&1')
                            time.sleep(10)
                            os.system("atcom --port " + str(serialDevice) + " -b 19200 AT+CHUP >/dev/null 2>&1")
                    if not line:
                        break

            # Wait 3s for the nest loop
            print("-----------------------\n\n")
            time.sleep(3)

finally:
    # We don't have connection. We must signal the state to the kernel, and close the device
    phone.close()
