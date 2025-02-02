import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI"}


def test_read_accident():
    response = client.get("/api/accident/")
    res_dict = response.json()
    key_lst = ['date', 'time', 'accident_type', 'airline', 'fatalities', 'occupants', 'aircraft_status', 'location', 'phase', 'description', 'ko_description']
    
    assert response.status_code == 200
    assert set(key_lst).issubset(res_dict.keys())


def test_read_accidents():
    start = 0
    size = 10
    response = client.get(f"/api/accidents?start={start}&size={size}")
    res_dict = response.json()
    key_lst = ['_id', 'date', 'fatalities', 'aircraft_status', 'location', 'time', 'airline', 'occupants']
    
    assert response.status_code == 200
    assert len(res_dict) == 10
    for i in range(len(res_dict)):
        assert set(key_lst).issubset(res_dict[i].keys())


def test_read_airline_suggestions_exist():
    airline = "Jeju%20Air"
    response = client.get(f"/api/suggestions/{airline}")
    res_dict = response.json()
    assert response.status_code == 200
    assert len(res_dict) >= 1
    
    
def test_read_airline_suggestions_no_exist():
    airline = "NoExistAirline"
    response = client.get(f"/api/suggestions/{airline}")
    res_dict = response.json()
    assert response.status_code == 200
    assert len(res_dict) == 0


def test_read_airline_info_exist():
    airline = "Jeju%20Air"
    response = client.get(f"/api/information/{airline}")
    res_dict = response.json()
    key_lst = ['date', 'time', 'accident_type', 'airline', 'fatalities', 'occupants', 'aircraft_status', 'location', 'phase', 'description', 'ko_description', '_id']
    
    assert response.status_code == 200
    assert len(res_dict) >= 1
    for i in range(len(res_dict)):
        assert set(key_lst).issubset(res_dict[i].keys())
    
    
def test_read_airline_info_no_exist():
    airline = "NoExistAirline"
    response = client.get(f"/api/information/{airline}")
    res_dict = response.json()
    key_lst = ['date', 'time', 'accident_type', 'airline', 'fatalities', 'occupants', 'aircraft_status', 'location', 'phase', 'description', 'ko_description', '_id']
    
    assert response.status_code == 200
    assert len(res_dict) == 0
    for i in range(len(res_dict)):
        assert set(key_lst).issubset(res_dict[i].keys())
        

def test_read_airline_description_exist():
    _id = "Cn-QwZQBZYMe0_8tPeyo"
    response = client.get(f"/api/description/{_id}")
    res_dict = response.json()
    
    assert response.status_code == 200
    assert "description" in res_dict


def test_read_airline_description_no_exist():
    _id = "no_exist_id"
    response = client.get(f"/api/description/{_id}")
    res_dict = response.json()
    
    assert response.status_code == 200
    assert len(res_dict) == 0
    

def test_read_airline_ko_description():
    _id = "7eYWjpQBsnp6W0Xd8Zpo"
    response = client.get(f"/api/ko_description/{_id}")
    
    assert response.status_code == 200


def test_check_ko_description():
    _id = "7eYWjpQBsnp6W0Xd8Zpo"
    response = client.get(f"/api/check_ko_description/{_id}")
    res_dict = response.json()
    
    assert response.status_code == 200
    assert "ko_description_empty" in res_dict