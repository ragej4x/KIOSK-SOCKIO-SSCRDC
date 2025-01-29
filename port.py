import wmi

def list_usb_devices():
    c = wmi.WMI()

    usb_devices = c.query("SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE '%USB%'")

    if not usb_devices:
        print("No USB devices found.")
    else:
        print("Connected USB Devices:")
        for device in usb_devices:
            try:
                device_id = device.DeviceID
                description = device.Description if device.Description else "Unknown Device"

                # Extract VID and PID if present in DeviceID
                if "VID_" in device_id and "PID_" in device_id:
                    vendor_id = device_id.split("VID_")[1][:4]
                    product_id = device_id.split("PID_")[1][:4]

                    print(f"Device: {description}")
                    print(f"Vendor ID: {vendor_id}, Product ID: {product_id}")
                else:
                    print(f"Device: {description} does not contain VID/PID info.")
                print("-" * 40)
            except Exception as e:
                print(f"Error processing device: {e}")

# Call the function
list_usb_devices()
