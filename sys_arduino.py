import serial, json

ser = serial.Serial('COM4', 9600)
print("Connected to Arduino")



#system calculation logic
class sys_info():
    def __init__(self):
        self.credit = 0
        self.to_pay = 0
        self.change = None
        self.status = False
        self.deduct = 0

    def calculate(self):
        with open('receipt.json') as file:
            data = json.load(file)
            self.to_pay = data['total_price']
        

        self.deduct = self.credit - self.to_pay

        self.to_pay = self.to_pay - self.credit
        
        if self.to_pay <1:
            self.to_pay = 0

        if self.deduct > 0:
            self.change = self.deduct
        

    def update(self):

        while True:
            self.calculate()
            print(f"Cash  {self.credit} : To pay  {self.to_pay} :  Change  {self.change} : Status  {self.status} ")

            ser_data = ser.readline().decode('utf-8').strip()
            self.credit += int(ser_data)



system = sys_info()


if __name__ == "__main__":
    system.update()