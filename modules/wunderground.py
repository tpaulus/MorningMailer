#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import lib.requests as Requests
from properties import Property


class Weather(object):
    def __init__(self, city, state, units='f'):
        self.city = city
        self.state = state
        if units == 'f':
            self.units = 'English'
        else:
            self.units = 'Metric'
        self.token = Property.wunderground_api_key
        self.json = []
        self.forecast = ''
        self.weather_icon = ''
        self.map_url = 'http://api.wunderground.com/api/%s/animatedradar/q/%s/%s.gif?width=560&height=480' \
                       '&newmaps=1&noclutter=1' % (self.token, self.state, self.city)

    def get_data(self):
        """
        get data for the location
        :return: JSON object
        """

        d = Requests.get(
            'http://api.wunderground.com/api/' + str(self.token) + '/forecast/q/' + str(self.state) + '/' + str(
                self.city) + '.json')
        self.json = d.json()
        self.text()

    def text(self):
        if self.units == 'English':
            text = 'fcttext'
        else:
            text = 'fcttext_metric'
        self.forecast = str(self.json['forecast']['txt_forecast']['forecastday'][0][text])
        self.weather_icon = str(self.json['forecast']['txt_forecast']['forecastday'][0]['icon_url'])

    def get_forecast(self):
        return self.forecast, self.weather_icon

    def get_map_url(self):
        return self.map_url


if __name__ == '__main__':
    state = raw_input("Enter your state with the standard 2 letter abbreviation, ie. CA: ")
    city = raw_input("Enter your city: ")
    w = Weather(city, state)
    w.get_data()
    print w.get_forecast()
    print w.get_map_url()
