import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"

@allure.feature("Pet")

class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"
#===============================================================================================================

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404,"Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"
#================================================================================================================
    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        pet_id = None
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "photoUrls": [],
                "status": "available"
            }
        try:
            with allure.step("Отправка запроса на создание питомца"):
                response = requests.post(url=f"{BASE_URL}/pet", json=payload)

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, "Код ответа питомца не совпадает с ожидаемым"
                response_json = response.json()
                pet_id = response_json["id"]

            with allure.step("Проверка структуры ответа по PET_SCHEMA"):
                jsonschema.validate(response_json, PET_SCHEMA)

            with allure.step("Проверка параметров питомца в ответе"):
                assert response_json['id'] == payload['id'], 'id не совпадает с ожидаемым'
                assert response_json['name'] == payload['name'], 'name не совпадает с ожидаемым'
                assert response_json['status'] == payload['status'], 'status не совпадает с ожидаемым'

            with allure.step("Проверка, что питомец действительно создан"):
                get_pet = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
                assert get_pet.status_code == 200,f"Питомец {pet_id} не найден"
                get_pet_json = get_pet.json()
                assert get_pet_json["id"] == pet_id, "id сохранённого питомца не совпадает"
                assert get_pet_json["name"] == payload["name"], "name сохранённого питомца не совпадает"
                assert get_pet_json["status"] == payload["status"], "status сохранённого питомца не совпадает"
        finally:
            if pet_id is not None:
                with allure.step("Удаление тестового питомца"):
                    requests.delete(f"{BASE_URL}/pet/{pet_id}")
#=======================================================================================================================
