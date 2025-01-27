<h1>Documentation for Integrating USB Devices with SOCKIO Checkout System
Overview</h1>
This documentation outlines the integration of USB devices (Arduino, bill acceptor, coin slot, coin hopper, and tablet) with the SOCKIO checkout system. The goal is to use USB detection and communication for managing hardware peripherals within the checkout application. It describes the use of PyWinUSB for detecting connected USB devices and ensuring their functionality can be verified.

<h2>Components</h2>
Hardware
Arduino Board: Interface for managing peripherals (bill acceptor, coin slot, coin hopper).
Bill Acceptor: Accepts bills and provides signals to the system for processing.
Coin Slot: Accepts coins and processes them as input for transactions.
Coin Hopper: Dispenses coins for change as part of the checkout system.
Tablet: Runs the SOCKIO system (using Pygame) to provide a UI for the checkout process.
Software
Python Modules:
pygame: Used for rendering the UI and handling interactions.
pywinusb: Used for detecting and communicating with USB devices.
csv and json: For generating receipts.
Device Communication Protocols:
USB HID for hardware communication with Arduino and other devices.
Environment Setup


1. Python Installation
Ensure Python 3.x is installed on your system. Verify installation by running:

bash
Copy
Edit

python --version

2. Install Dependencies
Install the required libraries for Pygame and USB communication:

bash
Copy
Edit
pip install pygame pywinusb
3. Connect Hardware
Connect the Arduino board, bill acceptor, coin slot, and coin hopper to the system via USB ports. Ensure proper drivers are installed for the devices.

Code Explanation
The integration includes three main functionalities:

USB Device Detection
Checkout System UI
Receipt Generation
1. USB Device Detection
The scan_usb_devices method in the SockioApp class detects connected USB devices. This functionality is implemented using pywinusb.

Code
python
Copy
Edit
def scan_usb_devices(self):
    """Scan for connected USB devices and store their details."""
    self.usb_devices = []  # Clear previous results
    all_devices = pywinusb.hid.HidDeviceFilter().get_devices()

    if all_devices:
        for device in all_devices:
            self.usb_devices.append({
                "name": device.product_name if device.product_name else "Unknown Device",
                "vendor_id": hex(device.vendor_id),
                "product_id": hex(device.product_id)
            })
    else:
        self.usb_devices.append({"name": "No devices found", "vendor_id": "", "product_id": ""})
Key Points
Scans for all USB HID devices connected to the system.
Stores the device name, Vendor ID, and Product ID.
Displays "No devices found" if no hardware is connected.
2. Checkout System UI
The checkout system is rendered using Pygame, with a button to trigger USB detection and display connected devices.

UI Code for Device List
python
Copy
Edit
def draw_checkout_page(self):
    screen.fill(BACKGROUND_COLOR)
    self.draw_header()

    # USB Device Detection Button
    usb_button = pygame.Rect(400, 500, 200, 50)
    pygame.draw.rect(screen, BUTTON_PROCEED_COLOR, usb_button, border_radius=10)
    usb_text = font.render("Scan Devices", True, BUTTON_TEXT_COLOR)
    screen.blit(usb_text, (usb_button.x + 40, usb_button.y + 10))

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if usb_button.collidepoint(mouse_pos) and mouse_click[0]:
        self.scan_usb_devices()

    # Display USB Devices
    start_y = 200
    for device in self.usb_devices:
        device_text = font_small.render(
            f"Name: {device['name']}, Vendor ID: {device['vendor_id']}, Product ID: {device['product_id']}", 
            True, TEXT_COLOR
        )
        screen.blit(device_text, (100, start_y))
        start_y += 30
Key Points
Displays a "Scan Devices" button for detecting connected hardware.
Lists detected USB devices, including names, Vendor IDs, and Product IDs.
3. Receipt Generation
Upon proceeding with checkout, receipts are generated in both CSV and JSON formats.

CSV Receipt Code
python
Copy
Edit
with open("receipt.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Item", "Quantity", "Price"])
    for item in self.cart_items:
        csvwriter.writerow([item["name"], item["quantity"], item["price"] * item["quantity"]])
JSON Receipt Code
python
Copy
Edit
receipt_data = {
    "items": self.cart_items,
    "total_price": sum(item["price"] * item["quantity"] for item in self.cart_items)
}
with open("receipt.json", "w") as jsonfile:
    json.dump(receipt_data, jsonfile, indent=4)
Hardware Interfacing with Arduino
To integrate with the Arduino for managing the bill acceptor, coin slot, and coin hopper:

Arduino Sketch:
Write an Arduino sketch to communicate with the Python application via USB (e.g., using Serial.print to send data about accepted coins and bills).
Python Communication:
Use pyserial for reading and writing data to the Arduino:
python
Copy
Edit
import serial

arduino = serial.Serial('COM3', 9600)  # Adjust COM port
data = arduino.readline().decode().strip()  # Read data from Arduino
print(data)
How the System Works
Checkout Process

Users add items to the cart.
Total price is displayed in the checkout screen.
USB Device Integration

Click "Scan Devices" to detect and display connected USB devices.
Devices such as Arduino, bill acceptor, and coin slot appear in the list.
Receipt Generation

Upon proceeding with checkout, a CSV and JSON receipt are generated, showing itemized details and the total price.
Bill and Coin Handling

The Arduino interfaces with the bill acceptor, coin slot, and coin hopper to handle payments and dispense change.
Python reads the input from Arduino and updates the UI accordingly.
