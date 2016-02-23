# -*- coding: utf-8 -*-
"""
Shows Bus leaving from Ulm university.

Show the departue of the next $x buses from
Ulm university. Data is obtained from the API
provided by ulmapi.de

Configuration parameters:
    - cache_timeout : How often we refresh this module in seconds.
    - line          : Which line to show.
    - filter_by_line: Show only one line of all.
    - busstop       : which stop (1240 is uulm sued)
    - limit         : Amount of next departures
    - maxdisplay    : How many to show in i3Bar
    - color         : Color of text (only py3status)
    - linestart     : Starting symbol of outputstring.

@author Martin Deubzer deubzerm@gmail.com
@license BSD
"""

# import your useful libs here
import json
import urllib.request
from time import time


class Py3status:
    """
    The Py3status class name is mendatory.
    """

    # available configuration parameters
    cache_timeout = 2
    #which line to show
    line = 3
    #filter for line provided above
    filter_by_line = True

    # busstop id of uulm http://h.fs-et.de/
    busstop = 1240 
    limit = 20
    maxdisplay = 3
    home_ssid = "OncIsInDaHouse"

    #color
    color = '#1F8CDE'
    ##symbols
    linestart = " "
    countdownsymbol = " "

    def __init__(self):
        self.count = 0
        """
        class constructor. 
        """
        
        pass

    def kill(self, i3s_output_list, i3s_config):
        """
        This method will be called upon py3status exit.
        """
        pass

    def departure(self, i3s_output_list, i3s_config):
        #json-data from api
        stops = self.getBus(self.busstop, self.limit)
        if stops != None:
            #filter for line
            filteredstops = self.filterBus(self.line, stops, self.filter_by_line)
        
            msg = self.constructMessage(filteredstops, self.maxdisplay)
        
            response = {
                'color' : self.color,
                'cached_until': time() + self.cache_timeout,
                'full_text': msg 
            }
        else:
            response = {
                'color': '#FF0000',
                'full_text': self.linestart+" "
            }

        return response

    def getBus(self, stop_id, limit):
        try:
            fset_api = "http://h.fs-et.de/api.php?id="+str(stop_id)+"&limit="+str(limit)
            request = urllib.request.Request(fset_api)
            response = urllib.request.urlopen(request)
            result = json.loads(response.read().decode('utf-8'))

            return result
        except Exception as e:
            print(e)
            return None

    def filterBus(self,line,json, filterbus):
        f_res = []

        res = json['departures']
        
        if filterbus:
            for item in res:
                if item['line'] == str(line):
                    f_res.append((item['line'],item['countdown']))
            #print(f_res)
            return f_res
        else:
            for item in res:
                f_res.append((item['line'],item['countdown']))
            f_res.sort(key=lambda tup: tup[0]) #sort for grouping
            #print(f_res) 
            return f_res

    def sortplan(self):
        tuplelist = self
        el = []
        while len(tuplelist) != 0:
            for item in tuplelist:
                print(item[0])
                


    def constructMessage(self, filterjson, maxdisplay):
        """
        constructs fulltextmessage from filtered json, show only up to
        maxdisplays
        """
        res = ""+self.linestart + str(self.line) + self.countdownsymbol
        for t in filterjson[:maxdisplay]:
            res = res + str(t[1]) + ", "

        #remove last", "
        return res[:-2]


if __name__ == "__main__":
    """
    Test this module by calling it directly.
    This SHOULD work before contributing your module please.
    """
    from time import sleep
    cache_timeout = 3
    x = Py3status()
    config = {
        'color_bad': '1F8CDE',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00',
        'busstop':'1240',
        'limit':'20',
        'line':'3'
    }
    """
    while True:
        print(x.departure([],config))
        #print(x.departure([],config)['full_text'])
        sleep(cache_timeout)
    """
    print(x.departure([],config)['full_text'])
