#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import requests as Requests
from properties import Property


class Weather(object):
    def __init__(self, units='f'):
        self.city = Property.user_city
        self.state = Property.user_state
        if units == 'f':
            self.units = 'English'
        else:
            self.units = 'Metric'
        self.token = Property.wunderground_api_key
        self.json = {}
        self.forecast = ''
        self.weather_icon = ''
        self.map_url = 'http://api.wunderground.com/api/%s/radar/q/%s/%s.png?width=560&height=480' \
                       '&newmaps=1&noclutter=1' % (self.token, self.state, self.city)

    def get_data(self):
        """
        get data for the location
        :return: JSON object
        """
        try:
            pkg = Requests.get(
                'http://api.wunderground.com/api/' + str(self.token) + '/forecast/q/' + str(self.state) + '/' + str(
                    self.city) + '.json')
            self.json = pkg.json()
        except:
            return False
        else:
            self.text()
            return self.json

    def text(self):
        """
        :return: str with text forecast
        """
        if self.units == 'English':
            text = 'fcttext'
        else:
            text = 'fcttext_metric'
        self.forecast = str(self.json['forecast']['txt_forecast']['forecastday'][0][text])
        self.weather_icon = str(self.json['forecast']['txt_forecast']['forecastday'][0]['icon_url'])
        return self.forecast

    def get_forecast(self):
        if self.forecast == '' and self.weather_icon == '':
            self.get_data()

        return self.forecast, self.weather_icon

    def get_map_url(self):
        return self.map_url


if __name__ == '__main__':
    w = Weather()
    w.get_data()
    print w.get_forecast()
    print w.get_map_url()