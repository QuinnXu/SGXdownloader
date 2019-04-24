from indexcrawler import getFileDate, createTable, addTable
from downloader import downloader
import logging

#get the latest index 
def getLatestIndex():
    f = open('indextable/latestindex.txt', 'r')
    a = f.read()
    f.close()
    if a == '':
        latestindex = 4340 # prepare for initializing
        latestdate = '20190329'
    else:
        latestindex = int(a.split(' ')[1])
        latestdate = a.split(' ')[0]

    done = 0
    # if index >= temp, the file on website is unavailable
    while not done:
        temp = getFileDate(latestindex+1)
        if temp == '0':
            done = 1
        else:
            latestdate = temp
            latestindex += 1

    f = open('indextable/latestindex.txt', 'w')
    f.write(latestdate + ' ' + str(latestindex))
    f.close()

# update latest index
def dailyUpdate():
    getLatestIndex()
    f = open('indextable/latestindex.txt', 'r')
    a = f.read().split(' ')
    f.close()
    date = a[0]
    index = a[1]
    addTable(index)
    downloader(date, index)

def recreateIndextable():
    getLatestIndex()
    f = open('indextable/latestindex.txt', 'r')
    a = f.read().split(' ')
    f.close()
    index = int(a[1])
    createTable(2755,index)
    #recovery
    f = open('indextable/indexmissed.txt', 'r')
    a = f.read().split(' ')
    f.close()
    for i in a:
        if i != '':
            addTable(int(i))
    print('Latest index created from 2755 to {}'.format(str(index)))
