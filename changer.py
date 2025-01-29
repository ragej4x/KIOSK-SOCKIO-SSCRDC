import serial
import json
import time

# Initialize the serial connection
ser = serial.Serial('COM4', 9600)
time.sleep(2)  # Wait for the connection to initialize

# Read the JSON file
with open('receipt.json', 'r') as file:
    data = json.load(file)

# Convert JSON data to string
data_string = json.dumps(data)

# Send JSON data to Arduino
ser.write(data_string.encode())
print(f"Sent: {data_string}")

# Close the serial connection
ser.close()
