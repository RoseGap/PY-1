import requests
import json
from datetime import datetime
from secrets import YA_DISK_TOKEN

def get_public_ip():
    response = requests.get("https://api.ipify.org")
    return response.text

def get_geo_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/geo")
    return response.json()

def save_to_json(data, filename="ip_info.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def upload_to_yandex_disk(token, file_path, disk_file_name):
    # Получаем ссылку для загрузки
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    params = {"path": disk_file_name, "overwrite": "true"}
    headers = {"Authorization": f"OAuth {token}"}

    response = requests.get(upload_url, headers=headers, params=params)
    upload_link = response.json().get("href")

    with open(file_path, "rb") as f:
        requests.put(upload_link, files={"file": f})


# Основная логика
if __name__ == "__main__":
    ip = get_public_ip()
    geo_data = get_geo_info(ip)
    geo_data["retrieved_at"] = datetime.now().isoformat()
    save_to_json(geo_data, "ip_info.json")
    upload_to_yandex_disk(YA_DISK_TOKEN, "ip_info.json", "ip_info.json")
    print("Данные успешно сохранены и загружены на Яндекс.Диск.")