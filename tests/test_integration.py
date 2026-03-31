from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
import pytest
from datetime import date
from src.models import Parameters, ApartmentSettlement, Bill


def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key

def test_tenants_in_manager():
    parameters = Parameters()
    manager = Manager(parameters)
    assert len(manager.tenants) > 0
    names = [tenant.name for tenant in manager.tenants.values()]
    for tenant in ['Jan Nowak', 'Adam Kowalski', 'Ewa Adamska']:
        assert tenant in names

def test_if_tenants_have_valid_apartment_keys():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.check_tenants_apartment_keys() == True

    manager.tenants['tenant-1'].apartment = 'invalid-key'
    assert manager.check_tenants_apartment_keys() == False
    
def test_get_apartment_cost():
    parameters = Parameters()
    manager = Manager(parameters)

    assert manager.get_apartment_cost('nonexistemt') is None
    
    assert manager.get_apartment_cost('apart-polanka', 2025, 1) == 910.0
    
    assert manager.get_apartment_cost('apart-polanka', 2025, 3) == 0.0
    total_year = manager.get_apartment_cost('apart-polanka', 2025)
    assert total_year >= 450.0

    total_all = manager.get_apartment_cost('apart-polanka')
    assert total_all >= total_year
    
    with pytest.raises(ValueError):
        manager.get_apartment_cost('apart-polanka', 2025, 13)

    with pytest.raises(ValueError):
        manager.get_apartment_cost('apart-polanka', 2025, 0)
        
def test_create_apartment_settlement():
    parameters = Parameters()
    manager = Manager(parameters)

    apartment_keys = ['apart-polanka']

    manager.bills = [
        Bill(apartment_key='apart-polanka', amount=100.0, date=date(2024, 3, 5)),
        Bill(apartment_key='apart-polanka', amount=200.0, date=date(2024, 3, 15)),
        Bill(apartment_key='apart-polanka', amount=150.0, date=date(2024, 4, 1)),
        Bill(apartment_key='apart-polanka', amount=300.0, date=date(2024, 3, 10)),
    ]

    settlement_march_apart_polanka = manager.create_apartment_settlement('apart-polanka', 2024, 3)
    settlement_april_apart_polanka = manager.create_apartment_settlement('apart-polanka', 2024, 4)
    settlement_march_apart_polanka = manager.create_apartment_settlement('apart-polanka', 2024, 3)
    settlement_no_bills = manager.create_apartment_settlement('apart-polanka', 2024, 4)

    assert isinstance(settlement_march_apart_polanka, ApartmentSettlement)
    assert isinstance(settlement_april_apart_polanka, ApartmentSettlement)
    assert isinstance(settlement_march_apart_polanka, ApartmentSettlement)
    assert isinstance(settlement_no_bills, ApartmentSettlement)

    assert settlement_march_apart_polanka.apartment_key == 'apart-polanka'
    assert settlement_april_apart_polanka.apartment_key == 'apart-polanka'
    assert settlement_march_apart_polanka.apartment_key == 'apart-polanka'
    assert settlement_no_bills.apartment_key == 'apart-polanka'

    assert settlement_march_apart_polanka.month == 3
    assert settlement_march_apart_polanka.year == 2024
    assert settlement_april_apart_polanka.month == 4
    assert settlement_april_apart_polanka.year == 2024

    assert settlement_march_apart_polanka.balance == 300.0
    assert settlement_april_apart_polanka.balance == 150.0
    assert settlement_march_apart_polanka.balance == 300.0
    assert settlement_no_bills.balance == 0.0  