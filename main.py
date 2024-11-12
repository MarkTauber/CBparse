from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import requests

TIMEOUT = 10


def get_cbr_data(date_req):
    """
    Функция для получения данных с API ЦБ РФ.

    Args:
        date_req (str): Дата запроса в формате "dd.mm.yyyy".

    Returns:
        dict: Словарь с данными о валютах.
    """
    url = f"http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={date_req}"
    response = requests.get(url, timeout=TIMEOUT)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        currencies = {}
        for valute in root.iter("Valute"):
            char_code = valute.find("CharCode").text
            if char_code not in currencies:
                currencies[char_code] = {
                    "NumCode": valute.find("NumCode").text,
                    "Name": valute.find("Name").text,
                    "Values": [],
                }
            currencies[char_code]["Values"].append(
                float(valute.find("Value").text.replace(",", "."))
            )
        return currencies

    print(
        f"Ошибка запроса к ЦБ РФ для {date_req}: {response.status_code}"
    ) 
    return None


def analyze_data(data):
    """
    Функция для анализа данных о валютах.

    Args:
        data (dict): Словарь с данными о валютах.

    Returns:
        dict: Словарь с результатами анализа.
    """
    results = {}
    for currency, info in data.items():
        if not info["Values"]:
            continue

        average = sum(info["Values"]) / len(info["Values"])
        minimum = min(info["Values"])
        maximum = max(info["Values"])

        min_date_index = info["Values"].index(minimum)
        max_date_index = info["Values"].index(maximum)

        start_date = datetime.now() - timedelta(
            days=len(info["Values"])
        )  # Correct calculation
        min_date = (start_date + timedelta(days=min_date_index)).strftime("%d.%m.%Y")
        max_date = (start_date + timedelta(days=max_date_index)).strftime("%d.%m.%Y")
        results[currency] = {
            "average": average,
            "minimum": minimum,
            "maximum": maximum,
            "min_date": min_date,
            "max_date": max_date,
        }
    return results


# Получаем данные за последние 90 дней
today = datetime.now()
data = {}
for i in range(90):
    current_date = today - timedelta(days=i)
    date_str = current_date.strftime("%d.%m.%Y")
    day_data = get_cbr_data(date_str)
    if day_data:
        for currency in day_data:
            if currency not in data:
                data[currency] = {
                    "NumCode": day_data[currency]["NumCode"],
                    "Name": day_data[currency]["Name"],
                    "Values": [],
                }
            data[currency]["Values"].extend(day_data[currency]["Values"])

# Анализ данных
analysis_results = analyze_data(data)

# Вывод результатов
for currency, result in analysis_results.items():
    print(f"Валюта: {currency} ({data[currency]['Name']})")
    print(f"Среднее: {result['average']:.4f}")
    print(f"Минимум: {result['minimum']:.4f} ({result['min_date']})")
    print(f"Максимум: {result['maximum']:.4f} ({result['max_date']})")
    print("-" * 20)
