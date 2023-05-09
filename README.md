# Check-GSM-Call

Check GSM call, validate Caller ID and deploy some action

This script, written in Python, allows you to interact with a GSM modem with AT commands, in order to:
1. Detect incoming voice calls;
2. Hang up the incoming voice call;
3. Check the caller_id of the origin of the voice call;
4. Validate if the caller_id is allowed, using the numbers in the numbers_permited.txt file;
5. If the caller_id is allowed, then perform the desired action (eg send SMS, run a program, run a script, call an entry controller, etc ....)

# Dependencies:

- ATCOM (pip3 install atcom)
