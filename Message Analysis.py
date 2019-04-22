mat# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 07:53:29 2019
Message analysis
@author: caleung
"""

import json
import pandas
import datetime as dt
import string
import random

filepath = r'C:\Users\caleung\Documents\PYTHON TESTING AREA\Messeges Analysis\message.json'
filepathout = r'C:\Users\caleung\Documents\PYTHON TESTING AREA\Messeges Analysis\cbmessage.csv'
filen = open(filepath, 'r')
data = json.load(filen)


#this is how to change from ms timestamp
messagedf = pandas.DataFrame(data['messages'], columns = ['content', 'sender_name', 'timestamp_ms', 'type'])

messagedf['timestamp_ms'] = pandas.to_datetime(messagedf['timestamp_ms'], unit='ms')

#OutputCSV = open(filepathout, 'w' )
#OutputCSVWriter = csv.writer(OutputCSV, delimeter ',', quotechar='"')
#
#for i in messagedf:
#    
#messagedf.to_csv(filepathout)

numberofmessages = messagedf['sender_name'].count()


numberofmessagesfromeach = messagedf.groupby('sender_name').size()

messagedf['splitcontent'] = messagedf['content'].str.split()



def turnlistoflisttoonelist(listoflist):
    listofwordsfrommessage = []
    for list1 in listoflist:
        for list2 in list1:
            listofwordsfrommessage.append(list2)
    return listofwordsfrommessage



#var = turnlistoflisttoonelist(messagedf['splitcontent'].values.tolist())


listofwordsfrommessage = []
def weirdstuffstripper(listofwords):
    newlist = []
    
    #this is how to translate
    intab = string.punctuation
    #because we want to delete... we just take out the var (outtabe)
    #outtab = 
    trantab = str.maketrans(dict.fromkeys(string.punctuation))
    #then you use str.translate(trantab, 'xm')
    #first i need to put all the words in the list 
    for word in listofwords:
        for i in intab:
#            print(i)
            word1 = word.translate(trantab)
#            print(word1)
        newlist.append(word1.upper())

    return newlist
       
#actuallist = weirdstuffstripper(var)

#cat = ['cat!123', 'leung123%', 'dog#$%']
#print(weirdstuffstripper(cat))
#print( cat[:cat.find('!')]+cat[cat.find('!')+1:])


#$messagedf['uppersplitcontent'] = messagedf['splitcontent'].str.upper()
#how many times have we said SAD


def wordcounterinlist(listofstuff, word):
    counter = 0
    for i in listofstuff:
        if i.find(word) != -1:
            counter= counter+1
    return counter



#def WordCounterDictinlistoflist(listofstuff):
#    WordDict = {}
#    for message in listofstuff:
#        for word in message:
#            WordDict[word] = WordDict.setdefault(word, 0) + 1

def WordCounterDictinlist(listofstuff):
    WordDict = {}
    for word in listofstuff:
        WordDict[word] = WordDict.setdefault(word, 0) + 1
    return WordDict

#listtoputincounter = weirdstuffstripper(turnlistoflisttoonelist(messagedf['splitcontent'].values.tolist()))

WordCounterDictinlistreal = WordCounterDictinlist(weirdstuffstripper(turnlistoflisttoonelist(messagedf['splitcontent'].values.tolist())))          

def print_hist(diction, maxlines):
    counter = 0
    for i in sorted(diction, key=diction.get, reverse=True):
        print (i, diction[i])
        counter = counter +1
        if counter > maxlines:
            break
def print_hist2(diction, maxlines):
    t = []
    for i in sorted(diction, key=diction.get, reverse=True):
        t.append([i, diction[i]])
    for x,y in t[:maxlines]:
        print(x, y, sep = '\t')

               
print_hist(WordCounterDictinlistreal, 20)       
        
print_hist2(WordCounterDictinlistreal, 20)

#how to find spelling mistakes.....

Dictionaryreader = open(r'C:\Users\caleung\\Documents\New York Times Crosswords Accepted word list for use in Word Games.txt', 'r')
Dictionary= []
for i in Dictionaryreader:
    Dictionary.append(i.strip().upper())

def realwords(dictofwords):
    realwordslist = []
    notrealwordslist = []
    for word in dictofwords:
        if word in Dictionary:
            realwordslist.append(word)
        else:
            notrealwordslist.append(word)
    output1 = WordCounterDictinlist(realwordslist)
    output2 = WordCounterDictinlist(notrealwordslist)
    print('There are '+str(len(output1))+ ' real unique words in the messages with total occurance at'+str(sum(output1.values()))+ 'and there are ' + str(len(output2)) + 'unique not real unique words with the total at ' +str(sum(output2.values())))
    return output1,output2

#
#realwords(WordCounterDictinlistreal)
#

#random module also provides function to generate random values from continous distributions including Gaussian, exponential, gamma and a few more

#it should return a random value from the histogram, with the probability in proportion to its frequency

def choosefromhist1(histogdict):
    #so for input you have a dictionary of key value: word - counters
    #first you need the sum of everything to find the total
    #Sumofallcounters = sum(histog.values())
    #i guess now you will need to make it choose randomly.... I could do this 2 ways... the more efficent one would be to use the probabilities
    #or i can just force it to run through all the values... 
    #actually that may be way easier maybe not as efficent
    cumilativelist = []
    for i in histogdict:
        for x in range(histogdict[i]):
            cumilativelist.append(i)
    return random.choice(cumilativelist)
        
#testdic = {'key1': 1,'key2': 5,'key3': 7}

#print(choosefromhist1(WordCounterDictinlistreal))

#test = 'word'
#
#print(test.strip('w'))





#placeholder =messagedf['sender_name'].values.tolist()


#how many times have we said sad
#sadcounter = wordcounterinlist(messagedf['content'].values.tolist(), 'sad')            
#            
#            
#
##how many times have we said sad
#happycounter = wordcounterinlist(messagedf['content'].values.tolist(), 'happy')            
#    
#
##how many times have we said morning
#morningcounter = wordcounterinlist(messagedf['content'].values.tolist(), 'morning')            
#                    
#

    
    



#messagedf['sender_name'].count('Brianna Hugh')


#things i want to know
#how many messages
#distribution per month
#message per person