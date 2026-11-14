import pytest
import requests
BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"
#BASE_URL = "https://petstore.swagger.rv-school.ru"
@pytest.fixture(scope="function")
def create_pet():
#фикстура для создания питомца
    payload = {
        "id": 1,
        "name": "Boddy",
        "photoUrls": [],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200, f"Не удалось создать питомца: {response.status_code} {response.text}"
    pet_data = response.json()
    yield pet_data

    delete_response = requests.delete(f"{BASE_URL}/pet/{pet_data['id']}")
    assert delete_response.status_code in (200, 204, 404),f"Не удалось очистить питомца {pet_data['id']}: {delete_response.status_code} {delete_response.text}"
