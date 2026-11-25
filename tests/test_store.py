import allure
import jsonschema
import pytest
import requests

from .schemas.store_schema import ORDER_SCHEMA, INVENTORY_SCHEMA
BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"
@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_place_order(self):
        payload = {
            "id": 1,
            "petId": 1,
            "quantity": 1,
            "status": "placed",
            "complete": True,
        }
        with allure.step("Отправка запроса на создание заказа"):
            post_response = requests.post(url=f"{BASE_URL}/store/order", json=payload, timeout=10)
            post_response_json = post_response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert post_response.status_code == 200,  (
                f"Код ответа {post_response.status_code}, ожидался 200"
            )
            jsonschema.validate(post_response_json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            for key in ("id", "petId", "quantity", "status", "complete"):
                 assert post_response_json[key] == payload[key], (
                    f"Поле {key!r}: {post_response_json[key]!r}, "
                    f"ожидалось {payload[key]!r}"
                    )
#=================================================================================================================

    PLACE_ORDER_CASES = [
        pytest.param("placed", 200, id="placed"),
        pytest.param("approved", 200, id="approved"),
        pytest.param("delivered", 200, id="delivered"),
    ]
    @allure.title("Размещение заказа со статусом {status!r}")
    @pytest.mark.parametrize("status, expected_status_code", PLACE_ORDER_CASES)
    def test_place_order(self, status, expected_status_code, cleanup_order_id_1):
        payload = {
            "id": 1,
            "petId": 1,
            "quantity": 1,
            "status": status,
            "complete": True,
        }
        with allure.step(f"Отправка запроса на создание заказа со статусом {status!r}"):
            post_response = requests.post(f"{BASE_URL}/store/order", json=payload, timeout=10)

        with allure.step("Проверка статуса ответа"):
            assert post_response.status_code == expected_status_code, (
                f"Статус {status!r}: код {post_response.status_code}, "
                f"ожидался {expected_status_code}"
            )
        if expected_status_code == 200:
            with allure.step("Валидация JSON-схемы и полей ответа"):
                post_response_json = post_response.json()
                jsonschema.validate(post_response_json, ORDER_SCHEMA)
                for key in ("id", "petId", "quantity", "status", "complete"):
                    assert post_response_json[key] == payload[key], (
                        f"Поле {key!r}: {post_response_json[key]!r}, "
                        f"ожидалось {payload[key]!r}"
                    )


    @allure.title("Размещение заказа с невалидным статусом 'unknown'")
    def test_place_order_with_invalid_status(self, cleanup_order_id_1):
        payload = {
            "id": 1,
            "petId": 1,
            "quantity": 1,
            "status": "unknown",
            "complete": True,
        }
        with allure.step("Отправка запроса с невалидным статусом 'unknown'"):
            post_response = requests.post(f"{BASE_URL}/store/order", json=payload, timeout=10)
        with allure.step("Проверка статуса ответа — по контракту ожидается 400"):
            assert post_response.status_code == 400, (
                f"Код {post_response.status_code}, ожидался 400 "
                f"(стенд принимает невалидный статус — баг API)"
        )

#========================================================================================================================================

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        order_id = create_order["id"]

        with allure.step("Отправка запроса на получение заказа по ID"):
            get_response = requests.get(f"{BASE_URL}/store/order/{order_id}", timeout=10)

        with allure.step("Проверка статуса ответа"):
            assert get_response.status_code == 200, f"Код ответа {get_response.status_code}, ожидался 200"

        with allure.step("Проверка данных заказа"):
            get_response_json = get_response.json()
            assert get_response_json["id"] == order_id, (
                    f"Поле 'id': {get_response_json['id']!r}, "
                    f"ожидалось {order_id!r}"
            )

        with allure.step("Валидация JSON-схемы"):
            jsonschema.validate(get_response_json, ORDER_SCHEMA)

#=======================================================================================================================

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа"):
            delete_response = requests.delete(f"{BASE_URL}/store/order/{order_id}", timeout=10)

        with allure.step("Проверка статуса ответа"):
            assert delete_response.status_code == 200, f"Код ответа {delete_response.status_code}, ожидался 200"

        with allure.step("Проверка, что заказ больше не находится"):
            get_response = requests.get(f"{BASE_URL}/store/order/{order_id}", timeout=10)
            assert get_response.status_code == 404, (
                f"Заказ {order_id} всё ещё существует: "
                f"код {get_response.status_code}"
            )

#=======================================================================================================================

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):

        with allure.step("Отправка запроса на получение несуществующего заказа"):
            get_response = requests.get(f"{BASE_URL}/store/order/9999", timeout=10)

        with allure.step("Проверка статуса ответа"):
            assert get_response.status_code == 404, f"Код ответа {get_response.status_code}, ожидался 404"

        with allure.step("Проверка текстового содержимого ответа"):
            assert get_response.text == "Order not found", f"Текст ответа {get_response.text!r}, ожидалось 'Order not found'"

#=======================================================================================================================

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):

        with allure.step("Отправка запроса на получение инвентаря"):
            get_response = requests.get(f"{BASE_URL}/store/inventory", timeout=10)

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert get_response.status_code == 200, (
                f"Код ответа {get_response.status_code} , ожидался 200"
            )
            get_response_json = get_response.json()
            jsonschema.validate(get_response_json, INVENTORY_SCHEMA)

#=======================================================================================================================