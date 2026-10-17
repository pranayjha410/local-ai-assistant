
import requests

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url,timeout=10)
    return response.text


TOOLS = [
 
    {
          "type": "function",
                "function": {
                    "name": "get_city_weather",
                    "description": "Get the current weather for given city.",
                    "parameters": {
                        "type": "object",
                        "properties":{
                            "city":{
                                "type":"string",
                                "description": "City to get weather for."
                            }
                        }
                    }
                }
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {

    "get_city_weather": get_city_weather
}
