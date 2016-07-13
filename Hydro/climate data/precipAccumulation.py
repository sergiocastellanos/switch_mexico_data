import forecastio
import datetime
import json, pickle
from stats import Statistics as stats
from termcolor import colored

seasonlist = ["Winter","Spring","Summer","Autumn"]


class PrecipAccumulation:
    def retrievePickle(self):
        '''Opens a .pkl file and returns a dictionary'''
        precipAccumulation = pickle.load( open( "precipIntensity.pkl", "rb" ) )
        return precipAccumulation

    def monthly(self):
        '''Returns a monthly classification of a given dictionary (containing the precipAccumulation levels)'''
        monthlyRecord = {}
        precipAccumulationRecords = self.retrievePickle() #open the .pkl file an obtains the dictionary
        for year in range(2006,2016):
            for month in range(01,12):
                humonth = []
                for day in range(1,31):
                    try :
                        date = datetime.datetime(year,month,day)
                        humonth.append(precipAccumulationRecords[str(date.date())])
                    except ValueError:
                        pass
                s = stats(humonth)
                monthAverage = s.media()
                monthlyRecord[str(date.date())[:7]] = monthAverage
        return monthlyRecord

    def seasony(self,monthlyRecord):
        '''Returns season by classification of a given dictionary that is monthlyy clasified'''
        data = {}
        for year in range(2006,2016):
            seasons = {}
            a = 0
            for i in range(1,12,3):
                aux = []
                season = []
                for month in range(i,i+3):
                    try :
                        date = datetime.datetime(year,month,1)
                        aux.append(monthlyRecord[str(date.date())[:7]])
                    except KeyError:
                        pass
                s = stats(aux)
                seasonAverage = s.media()
                seasons[seasonlist[a]] = seasonAverage
                a+=1
            data[year] = seasons
        return data

    def get_data(self):
        '''This function acctualy return data classified by season'''
        data = self.seasony(self.monthly())
        return data



def printer(data):
    '''this function prints all the results of the precipAccumulation levels classified by season'''
    for element in data:
        print colored(element,color="magenta")
        for e in data[element]:
            print colored(e, color="white"), colored("%.5s"%data[element][e],color="cyan")


if __name__ == '__main__':
    printer(seasony(monthly()))
