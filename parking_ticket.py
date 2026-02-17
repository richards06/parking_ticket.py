import math

class ParkedCar:
    def __init__(self, make, model, color, license_number, minutes_parked):
        self.make = make
        self.model = model 
        self.color = color
        self.license_number = license_number
        self.minutes_parked = minutes_parked
        
class PoliceOfficer:
    def __init__(self, name, badge_number):
        self.name = name
        self.badge_number = badge_number
        
    def issue_ticket(self, car, meter):
        if car.minutes_parked > meter.minutes_purchased:
            overtime = car.minutes_parked - meter.minutes_purchased
            return overtime 
        else:
            return 0
        
class ParkingMeter:
    def __init__(self, minutes_purchased):
        self.minutes_purchased = minutes_purchased
        
def main():
    car = ParkedCar("Toyota", "Camry", "Black", "ABC123", 125)
    meter = ParkingMeter(60)
    officer = PoliceOfficer("Smith", "4578")
    
    overtime = officer.issue_ticket(car,meter)
    
    if overtime > 0:
        ticket = ParkingTicket(overtime)
        print("Ticket issued.")
        print("Overtime minutes:", overtime)
        print("Fine: $", ticket.fine)
    else:
        print("No violation.")
        
class ParkingTicket:
    def __init__(self, overtime_minutes):
        self.overtime_minutes = overtime_minutes
        self.fine = self.calculate_fine()
        
    def calculate_fine(self):
        hours = math.ceil(self.overtime_minutes / 60)
        
        if hours <= 1:
            return 25
        else:
            return 25 + (hours - 1) * 10

    
main()