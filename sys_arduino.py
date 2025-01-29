import serial, json
from print import pussy

"""!!! PALITAN NYO PO UNG PORT KUNG ANONG COMPORT NYO SA ARDUINO IDE !!!"""
"""             ETO  ↓↓↓↓   """
ser = serial.Serial('COM5', 9600)
print("Connected to Arduino")


# System calculation logic
class sys_info():
    def __init__(self):
        self.credit = 0
        self.to_pay = 0
        self.change = 0
        self.status = False
        self.deduct = 0
        self.total = 0
        self.get_change = None

    def calculate(self):
        with open('receipt.json') as file:
            data = json.load(file)
            self.to_pay = data['total_price']
            self.get_change = data["get_change"]

        self.deduct = self.credit - self.to_pay

        self.to_pay = self.to_pay - self.credit
        
        if self.to_pay < 1:
            self.to_pay = 0
            

        if self.deduct > 0:
            self.change = self.deduct

    def update_receipt(self):
        with open('receipt.json', "r") as file:
            data = json.load(file)

        data['to_pay'] = self.to_pay
        data['change'] = self.change
        data['cash'] = self.credit
        data['status'] = self.status
        

        with open('receipt.json', "w") as file:
            json.dump(data, file, indent=4)

    def update(self):
        while True:
            ser_data = ser.readline().decode('utf-8').strip()
            
            if ser_data.isdigit():  
                self.credit += int(ser_data)
                print(f"Detected bill amount: {self.credit}")
                self.status = True

                self.calculate()
                

                print(f"Cash: {self.credit} | To pay: {self.to_pay} | Change: {self.change} | Status: {self.status}")

                if not self.change < 1 :
                    self.change_trigger()
                    print("Sent change to the system.")
                    self.update_receipt()
                    pussy.print_receipt()
                    self.status = True
                    break
                
                elif not self.change < 1 and self.status == True:
                    self.update_receipt()
                    pussy.print_receipt()
                    self.status = True

                    break
                
                elif self.to_pay < 1:
                    self.update_receipt()
                    pussy.print_receipt()
                    self.status = True

                    break
                
    def change_trigger(self):
        ser.write(str(self.change).encode())  


system = sys_info()

system.update()