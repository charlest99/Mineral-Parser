import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from time import sleep
import random
import sys


def query_site(url):
    website = get(url).text
    swoop = BeautifulSoup(website, 'html.parser')
    return swoop

def createDf(names, indexes):
    df = pd.DataFrame(names, index = indexes, columns = ['Mineral Name'])  #gets all links for info pages on each mineral
    ikeys = list()
    url = 'https://www.minerals.net/mineral/almandine.aspx'
    swoop = query_site(url)
    ifields = swoop.find_all('td', class_ = 't1')
    for j in range (len(ifields)):
        x = ifields[j].text
        x = BeautifulSoup(x, 'html.parser')
        ikeys.append(x.prettify()) 
    for key in ikeys:
        df[key.strip()] = '0' #gets column names from mineral with every possible data field as some have fields missing
    return df

def getDict(swoop, typeClass):
    data = list()
    fields = swoop.find_all('td', class_ = typeClass) #finds all the info fields for a mineral
    for j in range (len(fields)):
        x = fields[j].text
        x = BeautifulSoup(x, 'html.parser')
        data.append(x.prettify()) #treats fields as keys to be zipped with corresponding value
    return data

def minToCSV(inp):

    url = 'https://www.minerals.net/Minerals/' + inp +'.aspx'
    swoop = query_site(url)

    mineralBin = swoop.find_all('a', class_ = 'bluelink') #finds all mineral names for a letter

    names = list()
    for i in range(len(mineralBin)):
        names.append(mineralBin[i].text)
        
    links = list()
    indexes = list(range(len(mineralBin)))
    for i in range(len(mineralBin)):
        links.append("https://www.minerals.net/" + mineralBin[i].attrs['href'])
    
    df =createDf(names,indexes)
    
    for i in range(len(links)):
        swoop = query_site(links[i]) #checks each minerals individual site
    
        keys = getDict(swoop, 't1')
        values = getDict(swoop, 't2')
        dict1 = dict(zip(keys, values)) #puts keys and values in dictionary
        for key in dict1.keys():
            df.at[i, key.strip()] = dict1[key].strip() #reset values of dataframe at mineral i at each field name with data
        
        time_to_wait = random.uniform(1,2)
        sleep(time_to_wait)
        
    df.to_csv(inp+'MineralsInfo.csv')

if __name__ == '__main__':
    minToCSV(str(input("Enter a letter for minerals.")))
    