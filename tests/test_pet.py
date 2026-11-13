import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"
#BASE_URL = "https://petstore.swagger.rv-school.ru"

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
#======================================================================================================================

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "photoUrls": [],
                       "status": "available"
                       }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404,"Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"
#======================================================================================================================

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

    @allure.title("Получение информации о питомце по id")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по id"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id
#=======================================================================================================================

    @allure.title("Изменение информации о питомце по id")
    def test_put_pet_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления"):
            updated_data_pet = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на получение информации о питомце по id"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "ожидается 200"
            assert response.json()["id"] == pet_id

        with allure.step("Отправка запроса на обновление информации о питомце"):
            put_response = requests.put(url=f"{BASE_URL}/pet", json=updated_data_pet)

        with allure.step("Проверка статуса и тела ответа"):
            assert put_response.status_code == 200, "ожидается 200"
            put_pet_json = put_response.json()
            assert put_pet_json["id"] == pet_id, "id не совпадает"
            assert put_pet_json["name"] == "Buddy Updated", "name не совпадает"
            assert put_pet_json["status"] == "sold", "status не обновился"

        with allure.step("Проверка, что изменения сохранены"):
            verify_changes = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert verify_changes.status_code == 200, "Проверка, что изменения сохранены"
            verify_changes_json = verify_changes.json()
            assert verify_changes_json["id"] == pet_id, "id изменился после PUT"
            assert verify_changes_json["name"] == "Buddy Updated", "name не сохранился"
            assert verify_changes_json["status"] == "sold", "status не сохранился"
#======================================================================================================================

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload =  {"id": 1,
                        "name": "Buddy",
                        "photoUrls": [],
                        "status": "available"
                    }
        with allure.step("Отправка запроса на создание питомца"):
            post_response = requests.post(url=f"{BASE_URL}/pet", json=payload)
        with allure.step("Проверка статуса ответа"):
            assert post_response.status_code == 200,f"Не удалось создать питомца: {post_response.status_code} {post_response.text}"
            post_response_json = post_response.json()
            pet_id = post_response_json["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            delete_response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert delete_response.status_code == 200,  f"Не удалось удалить питомца {pet_id}: {delete_response.status_code} {delete_response.text}"

        with allure.step("Проверка, что питомец действительно удален"):
            get_response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert get_response.status_code == 404,  f"Питомец {pet_id} всё ещё существует: {get_response.status_code} {get_response.text}"
#=======================================================================================================================




