from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_cost(self, apartment_key, year=None, month=None):
        if apartment_key not in self.apartments:
            return None
        
        if month is not None and (month < 1 or month > 12):
            raise ValueError(f"Invalid month: {month}. Must be between 1 and 12.")
        
        total_cost=0.0
        for bills in self.bills:
            if bills.apartment != apartment_key:
                continue
            if year is not None and bills.settlement_year != year:
                continue
            if month is not None and  bills.settlement_month != month:
                continue
            total_cost += bills.amount_pln

        return total_cost
    
    def create_apartment_settlement(self, apartment_key, year, month):
        total_bills = sum(
            bill.amount_pln
            for bill in self.bills
            if bill.apartment_key == apartment_key
            and bill.settlement_year == year
            and bill.settlement_month == month
        )
        total_transfers = 0.0

        return ApartmentSettlement(
            apartment_key=apartment_key,
            year=year,
            month=month,
            balance=total_transfers - total_bills
        )
        