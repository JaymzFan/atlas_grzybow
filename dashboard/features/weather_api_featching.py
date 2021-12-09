import requests

from typing import List
from datetime import datetime
from datetime import timedelta


def from_utc_unix(unix_timestamp: float, hour_shift: int = 0, output_day: bool = False) -> str:
    x = datetime.utcfromtimestamp(unix_timestamp)
    x = x + timedelta(hours=hour_shift)
    if output_day:
        return x.strftime('%Y-%m-%d')
    return x.strftime('%H:%M:%S')


class WeatherAPI:

    def __init__(self, API_KEY: str, base_url: str = "https://api.openweathermap.org/data/2.5/onecall"):
        self.API_KEY = API_KEY
        self.base_url = f"{base_url}?appid={API_KEY}&units=metric"

    @staticmethod
    def __transform_response(api_response: requests.Response) -> List:
        """
        Transforming api response into:
        Current weather info
        Daily weather info
        Hourly weather info
        """

        if api_response.status_code != 200:
            return []

        # transforming daily data
        res = api_response.json()
        hours_offset = int(int(res['timezone_offset'])/3600)

        next_days = res['daily']
        next_days = \
            [
                {
                    'dzien': from_utc_unix(unix_timestamp=x['sunrise'], hour_shift=hours_offset, output_day=True),
                    'wschod_slonca': from_utc_unix(unix_timestamp=x['sunrise'], hour_shift=hours_offset),
                    'zachod_slonca': from_utc_unix(unix_timestamp=x['sunset'], hour_shift=hours_offset),
                    'temperatura_poranek': round(x['temp']['morn'], ndigits=0),
                    'temperatura_poludnie': round(x['temp']['day'], ndigits=0),
                    'temperatura_wieczor': round(x['temp']['eve'], ndigits=0),
                    'temperatura_noc': round(x['temp']['night'], ndigits=0),
                    'temperatura_minimalna': round(x['temp']['min'], ndigits=0),
                    'temperatura_maksymalna': round(x['temp']['max'], ndigits=0),
                    'wilgotnosc': f"{x['humidity']} %",
                    'pogoda': x['weather'][0]['description'],
                    'zachmurzenie': f"{x['clouds']} %",
                    'prawdop_opadow': f"{round(x['pop']*100)} %"
                } for x in next_days
            ]

        return next_days

    def fetch_weather(self, lat: float, lon: float, exclude: str = 'minutely,alerts', lang: str = 'pl') -> List:
        request_link = f"{self.base_url}&lat={lat}&lon={lon}&exclude={exclude}&lang=pl"
        api_resp = requests.get(request_link)

        return self.__transform_response(api_response=api_resp)
