# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 09:05:29 2019
calvin and brianna facebook messages analysis
@author: Calvin
"""

import dateutil
import bs4
import pandas 
import json
import matplotlib.pyplot as plt
from string import punctuation
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()


pathtofile = r'C:\Users\Calvin\Pictures\crazy guy\message.json'

cannonbros =r'C:\Users\Calvin\Documents\Python stuff\Facebook Messages\CannonBrosmessage.json'

andyfile =r'C:\Users\Calvin\Documents\Python stuff\Facebook Messages\AndyCheungmessage.json'
exampleFile = open(pathtofile, 'r')
#exampleSoup = bs4.BeautifulSoup(exampleFile, "html.parser")

data = json.load(exampleFile)

cbmessagesdf = pandas.DataFrame(data['messages'], columns= ['content', 'sender_name', 'timestamp_ms', 'type'])

cbmessagesdf['timestamp_ms'] = pandas.to_datetime(cbmessagesdf['timestamp_ms'], unit = 'ms')

cbmessagesdf['Day of Week'] = cbmessagesdf['timestamp_ms'].dt.weekday
cbmessagesdfhour = cbmessagesdf
#cbmessagesdf['Datetime hours'] = cbmessagesdf['timestamp_ms'].to_period('H')
cbmessagesdfhour = cbmessagesdfhour.set_index('timestamp_ms')

#cbmessagesdfhour.asfreq(freq='1H', fill_value=0)
#Hourlytimedate = pandas.DataFrame()
#Hourlytimedate['numofmessagesperhourbree'] = cbmessagesdfhour.loc[lambda cbmessagesdfhour: cbmessagesdfhour['sender_name']=='Brianna Hugh'].resample('H').sum()

#Hourlytimedate['numofmessagesperhourclavin'] = cbmessagesdfhour.loc[lambda cbmessagesdfhour: cbmessagesdfhour['sender_name']=='Calvin Leung'].resample('H').sum()
#Hourlytimedate['Dayofweek']  = cbmessagesdfhour.resample('D').avg()

#Hourly.plot(style=[':', '--', '-'])
#plt.ylabel('Hourly count');





def fbmsgjsontopandasloader(filepath):
    usingfile = open(filepath, 'r')
    filedata = json.load(usingfile)
    filedatadf = pandas.DataFrame(filedata['messages'], columns= ['content', 'sender_name', 'timestamp_ms', 'type'])
    filedatadf['timestamp_ms'] = pandas.to_datetime(filedatadf['timestamp_ms'], unit = 'ms')

    filedatadf = filedatadf.set_index('timestamp_ms')

    
    return filedatadf


andyfiledf = fbmsgjsontopandasloader(andyfile)

def messagesperhourforpandas(datafr):
    datafr.index = datafr.index.floor('1H')

    messagesperpersonperday1 = datafr.groupby([datafr.index, 'sender_name']).agg(['count'])

    messagesperpersonperday1.columns = messagesperpersonperday1.columns.get_level_values(0)+ messagesperpersonperday1.columns.get_level_values(1)
#
    messagesperpersonperday1= messagesperpersonperday1.reset_index()
    messagesperpersonperday1['Day of Week'] = messagesperpersonperday1['timestamp_ms'].dt.weekday
#    messagesperpersonperday1['timeofday'] = messagesperpersonperday1['timestamp_ms'].dt.strftime('%A')
    return messagesperpersonperday1


def messagesperhourforpandashm(datafr):
    datafr.index = datafr.index.floor('1H')

    messagesperpersonperday1 = datafr.groupby([datafr.index, 'sender_name']).agg(['count'])

    messagesperpersonperday1.columns = messagesperpersonperday1.columns.get_level_values(0)+ messagesperpersonperday1.columns.get_level_values(1)
#
    messagesperpersonperday1= messagesperpersonperday1.reset_index()
    messagesperpersonperday1['Day of Week'] = messagesperpersonperday1['timestamp_ms'].dt.weekday
    messagesperpersonperday1['Hour of Day'] = messagesperpersonperday1['timestamp_ms'].dt.hour
#    messagesperpersonperday1['timeofday'] = messagesperpersonperday1['timestamp_ms'].dt.strftime('%A')
    return messagesperpersonperday1

andymsgperday = messagesperhourforpandas(andyfiledf)
andymsgperhour =  messagesperhourforpandashm(andyfiledf)

andymsgperhourpiv = pandas.pivot_table(andymsgperhour,values = 'contentcount', index= 'Day of Week', columns = 'Hour of Day', aggfunc=np.sum)
#trace = go.Heatmap(z=[andymsgperhour['contentcount'], andymsgperhour['Day of Week'],andymsgperhour['Hour of Day']])
data = andymsgperhourpiv
print(data)
ax = sns.heatmap(andymsgperhourpiv, linewidths=.5,cmap="YlGnBu")



#cbmessagesdf['Day of Week'] = cbmessagesdf['timestamp_ms'].dt.weekday

#groupbystuff

#print(cbmessagesdf.groupby(['timestamp_ms','sender_name']).agg(['count']).head(5))



#cbmessagesdf['date'] =  cbmessagesdf['timestamp_ms'].index.floor('1D')

#MonthDateDF = cbmessagesdf['timestamp_ms'].dt.year


#Monthdf = cbmessagesdf['timestamp_ms'].dt.month
#yeadf = cbmessagesdf['timestamp_ms'].dt.year
#
#cbmessagesMYCOL = pandas.concat([cbmessagesdf,Monthdf,yeadf], axis = 1)

#
#
#
##make a new dataframe where date is the index
#
cbmessagesDATEdf = cbmessagesdf.set_index('timestamp_ms')
#
##setting it to day
cbmessagesDATEdf.index = cbmessagesDATEdf.index.floor('1d')

messagesperpersonperday = cbmessagesDATEdf.groupby([cbmessagesDATEdf.index, 'sender_name']).agg(['count'])

messagesperpersonperday.columns = messagesperpersonperday.columns.get_level_values(0)+ messagesperpersonperday.columns.get_level_values(1)
#
messagesperpersonperday= messagesperpersonperday.reset_index()
#
##messagesperpersonperday.index = cbmessagesDATEdf.index.floor('1d')
#
#cleanup_names =  {"Calvin Leung": 1, "Brianna Hugh": 2}
#
#cmapp =  {"1": 'Blue', "2": 'red'}
#df.loc[lambda df: df['shield'] == 8]
#cbmessagesDATEdf = cbmessagesdf.set_index('timestamp_ms')
#messagesperpersonperday['sender_name'].replace(cleanup_names, inplace=True)

#thiis is the plot for messages per day
ax = messagesperpersonperday.loc[lambda messagesperpersonperday : messagesperpersonperday['sender_name'] == 'Calvin Leung'].plot.scatter(x=['timestamp_ms'], y=['contentcount'], label='calvin', c = 'blue')

#ax = df.plot.scatter(x='a', y='b', color='DarkBlue', label='Group 1');
#
messagesperpersonperday.loc[lambda messagesperpersonperday: messagesperpersonperday['sender_name']=='Brianna Hugh'].plot.scatter(x=['timestamp_ms'], y=['contentcount'], c='Red', label='Brianna', ax=ax)


ax2 = messagesperpersonperday.loc[lambda messagesperpersonperday : messagesperpersonperday['sender_name'] == 'Calvin Leung'].plot(x='timestamp_ms', y='contentcount', label='calvin', c = 'blue')

messagesperpersonperday.loc[lambda messagesperpersonperday: messagesperpersonperday['sender_name']=='Brianna Hugh'].plot(x='timestamp_ms', y='contentcount', c='Red', label='Brianna', ax=ax2)


breemsg = cbmessagesdf.loc[lambda cbmessagesdf: cbmessagesdf['sender_name']=='Brianna Hugh']

breemsglist = breemsg['content'].str.split().values.tolist()

#values.tolist()
#

breedict = {}
for i in breemsglist:
    #add in dict

    for x in i:
        x = x.upper()
        x = x.strip(punctuation)
        breedict[x] = breedict.setdefault(x,1)+1
    
breedictdf= pandas.DataFrame.from_dict(breedict, orient ='index', columns = ['wordcount'])

#calvin

calvinmsg = cbmessagesdf.loc[lambda cbmessagesdf: cbmessagesdf['sender_name']=='Calvin Leung']

calvinmsglist = calvinmsg['content'].str.split().values.tolist()

#values.tolist()
#

caldict = {}
for i in calvinmsglist:
    #add in dict

    for x in i:
        x = x.upper()
        x = x.strip(punctuation)
        caldict[x] = caldict.setdefault(x,1)+1
    
caldictdf= pandas.DataFrame.from_dict(caldict, orient ='index')

#cumilative sum


messagesperpersonperdaycalvin = messagesperpersonperday.loc[lambda messagesperpersonperday: messagesperpersonperday['sender_name']== 'Calvin Leung']
messagesperpersonperdayBrianna = messagesperpersonperday.loc[lambda messagesperpersonperday: messagesperpersonperday['sender_name']== 'Brianna Hugh']

messagesperpersonperdaycalvincumsum = messagesperpersonperdaycalvin['contentcount'].cumsum()

messagesperpersonperdaycalvinbriannacumsum = messagesperpersonperday['contentcount'].cumsum()
messagesperpersonperdaycalvinandycumsum = andymsgperday['contentcount'].cumsum()

messagesperpersonperday['cumilativesummsg'] = messagesperpersonperdaycalvinbriannacumsum
andymsgperday['cumilativesummsg'] = messagesperpersonperdaycalvinandycumsum

messagesperpersonperdaybriannacumsum = messagesperpersonperdayBrianna['contentcount'].cumsum()

messagesperpersonperdayBrianna['cumilativesummsg'] = messagesperpersonperdaybriannacumsum
messagesperpersonperdaycalvin['cumilativesummsg'] = messagesperpersonperdaycalvincumsum

ax1 = messagesperpersonperdaycalvin.plot(x='timestamp_ms', y = 'cumilativesummsg')

messagesperpersonperdayBrianna.plot(x='timestamp_ms', y = 'cumilativesummsg' , ax = ax1)

plt.figure()

ax5 = andymsgperday.plot(x='timestamp_ms', y = 'cumilativesummsg',scalex =True)

messagesperpersonperday.plot(x='timestamp_ms', y = 'cumilativesummsg' , ax = ax5)

plt.figure()


#lets just make a bar graph for total words sent and total unique words used for Calvin and brianna
breedictdf.sort_values(by = 'wordcount', ascending = False).iloc[:11].plot(kind='bar',color='Red', label='Brianna' );





#then we can make a modification to total words not in dictionary
ax3 = messagesperpersonperday.loc[lambda messagesperpersonperday : messagesperpersonperday['sender_name'] == 'Calvin Leung'].plot.scatter(x=['timestamp_ms'], y=['contentcount'], label='calvin-brianna', c = 'blue')

#ax = df.plot.scatter(x='a', y='b', color='DarkBlue', label='Group 1');
#
andymsgperday.loc[lambda andymsgperday: andymsgperday['sender_name']=='Calvin Leung'].plot.scatter(x=['timestamp_ms'], y=['contentcount'], c='Green', label='Andy-calvin', ax=ax3)

andymsgperday.loc[lambda andymsgperday: andymsgperday['sender_name']=='Andy Cheung'].plot.scatter(x=['timestamp_ms'], y=['contentcount'], c='purple', label='Andy', ax=ax3)
messagesperpersonperday.loc[lambda messagesperpersonperday: messagesperpersonperday['sender_name']=='Brianna Hugh'].plot.scatter(x=['timestamp_ms'], y=['contentcount'], c='Red', label='Brianna', ax=ax3)
fig = ax3.get_figure()
fig.savefig(r'C:\Users\Calvin\Pictures\crazy guy\foo.pdf', bbox_inches='tight')
fig = ax5.get_figure()
fig.savefig(r'C:\Users\Calvin\Pictures\crazy guy\foo2.pdf', bbox_inches='tight')
 
#
#
#
#
#
#bargraphplot = cbmessagesDATEdf['sender_name'].astype('category')
#
##bargraphplotgrouped= bargraphplot.
#
#
#cbmessagesDATEdf.index.value_counts()
#plt.figure()
#new = bargraphplot.index.value_counts()
#
#new.plot(style='k--', label='Series');
#
#
##exampleSoup = bs4.BeautifulSoup(pathtofile, "html.parser"'lxml',  features="lxml")
##
##dates = exampleSoup.findAll('span', {'class' : 'meta'})
###
##for date in dates:
##    data = date.content[0].split(",", 1)
##    print(data)
##    
##
##inner_contents = exampleSoup.find("div", recursive = True).find("div").find("div").contents
##
##temp = []
##for msg in inner_contents:
##    print(msg)
##
#
##elems = exampleSoup.select('body > div > div > div > div._3a_u > div._4t5n > div:nth-child(1) > div._3-96._2let > div > div:nth-child(2)')
##                           
##                           /html/body/div/div/div/div[2]/div[2]/div[15]/div[2]/div/div[2]
##                           <div>Omg</div>
##                           body > div > div > div > div._3a_u > div._4t5n > div:nth-child(1) > div._3-96._2let > div > div:nth-child(2)
##                           
##                           selector
#
## x path /html/body/div/div/div/div[2]/div[2]/div[1]/div[2]/div/div[2]
#
##body > div > div > div > div._3a_u > div._4t5n > div:nth-child(1) > div._3-96._2let > div > div:nth-child(2)
#
##msg_content = exampleSoup.find('div')
##
###msg_content = exampleSoup.select('body > div > div > div > div._3a_u > div._4t5n > div:nth-child(1) > div._3-96._2let > div > div:nth-child(2)')
##
###second one body > div > div > div > div._3a_u > div._4t5n > div:nth-child(2) > div._3-96._2let > div > div:nth-child(2)
##content = msg_content.text
##
##print(content)
