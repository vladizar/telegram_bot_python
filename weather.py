from pyowm import OWM

API_KEY = "your_OWM_api_key"

owm = OWM(API_KEY)
owm.configuration["language"] = "ru"

def get_weather(city):
    mgr         = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w           = observation.weather
    temp        = dict(real=w.temperature("celsius")["temp"], feels=w.temperature("celsius")["feels_like"])
    status      = w.detailed_status
    wind        = w.wind()
    
    if wind["deg"] >= 338 or wind["deg"] <= 22:
        wind["deg"] = "Северный"
    elif 22 < wind["deg"] < 68:
        wind["deg"] = "Северо-Восточный"
    elif 68 <= wind["deg"] <= 112:
        wind["deg"] = "Восточный"
    elif 112 < wind["deg"] < 158:
        wind["deg"] = "Юго-Восточный"
    elif 158 <= wind["deg"] <= 202:
        wind["deg"] = "Южный"
    elif 202 < wind["deg"] < 248:
        wind["deg"] = "Юго-Западный"
    elif 248 <= wind["deg"] <= 292:
        wind["deg"] = "Западный"
    else:
        wind["deg"] = "Северо-Западный"

    return f'В городе {city} сейчас 🌡{temp["real"]} градусов Цельсия, по ощущению — 🌡{temp["feels"]} градусов. {status.capitalize()}. Ветер 💨{wind["speed"]}м/с, {wind["deg"]}.'