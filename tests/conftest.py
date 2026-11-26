import pytest
import requests
BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"

#фикстура для создания питомца
@pytest.fixture(scope="function")
def create_pet():
    payload = {
        "id": 1,
        "name": "Boddy",
        "photoUrls": [],
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=payload, timeout=10)
    assert response.status_code == 200, f"Не удалось создать питомца: {response.status_code} {response.text}"
    pet_data = response.json()
    yield pet_data

    delete_response = requests.delete(f"{BASE_URL}/pet/{pet_data['id']}", timeout=10)
    assert delete_response.status_code in (200, 204, 404),f"Не удалось очистить питомца {pet_data['id']}: {delete_response.status_code} {delete_response.text}"


#фикстура для создания заказа
@pytest.fixture(scope="function")
def create_order():
    payload = {
        "id": 2,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": False,
    }
    post_response = requests.post(url=f"{BASE_URL}/store/order", json=payload, timeout=10)
    assert post_response.status_code == 200, (
        f"Не удалось создать заказ в фикстуре: "
        f"{post_response.status_code} {post_response.text}"
    )
    yield post_response.json()

    delete_response = requests.delete(url=f"{BASE_URL}/store/order/{payload['id']}", timeout=10)
    assert delete_response.status_code in (200, 204, 404), (
        f"Не удалось очистить заказ {payload['id']}: "
        f"{delete_response.status_code} {delete_response.text}"
    )

#фикстура для удаления заказа
@pytest.fixture(scope="function")
def cleanup_order_id_1():
    yield
    requests.delete(f"{BASE_URL}/store/order/1", timeout=10)