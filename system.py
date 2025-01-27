import win32print
import json

class PosSys():
    def __init__(self):
        self.printer_name = "POSPrinter POS58"  
        # Load  JSON data
        with open('receipt.json') as file:
            data = json.load(file)
        
        self.text_to_print = "SOCKIO - San Sebastian College \n Recoletos De Cavite\n\n =============================== \n\n\n"
        for item in data['items']:
            line = f"{item['name']} x {item['quantity']} - ${item['price']}"
            self.text_to_print += line.ljust(40) + "\n"  

        self.text_to_print += f"\n\n ===============================\n\n Total: ${data['total_price']} \n\n Thankyou For Purchasing\n\n\n".ljust(40)



        
        self.print_receipt()
        
        


    def print_receipt(self):
        try:

            # Open the printer
            printer = win32print.OpenPrinter(self.printer_name)
            win32print.StartDocPrinter(printer, 1, ("Receipt", None, "RAW"))
            win32print.StartPagePrinter(printer)

            win32print.WritePrinter(printer, b'\x1B\x40') 
            
            win32print.WritePrinter(printer, b'\x1B\x21\x00')  
            
            win32print.WritePrinter(printer, b'\x1B\x61\x01') 
            
            win32print.WritePrinter(printer, self.text_to_print.encode("utf-8"))
            
            win32print.WritePrinter(printer, b'\x1B\x21\x00')  # nomal size (reset)

            win32print.WritePrinter(printer, b'\x1B\x61\x00') 

            win32print.WritePrinter(printer, b'\n')
            
            win32print.WritePrinter(printer, b'\x1D\x56\x00')  
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)
            win32print.ClosePrinter(printer)
            print("Receipt printed successfully!")
        except Exception as e:
            print(f"Error: {e}")

            
            print("Receipt printed successfully!")
        except Exception as e:
            print(f"Error: {e}")

# Create an instance of PosSys to run
PosSys()
