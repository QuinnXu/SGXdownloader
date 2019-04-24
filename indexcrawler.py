import urllib
import logging

def getFileDate(index):
    url = 'https://links.sgx.com/1.0.0/derivatives-historical/'+str(index)+'/TC.txt'
    try:
        request = urllib.request.urlopen(url, timeout=10)
        filename = str(request.headers._headers[4][1])
        try:
            date = filename.split('_')[1].split('.')[0]
            logging.info('Index {} coordinates {}'.format(str(date),str(index)))
        #files dont exist
        except:
            date = '0'
            logging.info('Index {} is empty'.format((str(index))))
    #fail for unknown reason
    except Exception as e:
        logging.warning('Index {} is failure, {}'.format(str(index),str(e)))
        date = 'NA'
        f = open('indextable/indexmissed.txt', 'a')
        f.write(str(index)+' ')
        f.close()
    return date

def addTable(index):
    f = open('indextable/indextable.txt', 'r')
    a = f.read()
    index_table = eval(a)
    f.close()
    index_table[getFileDate(index)] = index
    f = open('indextable/indextable.txt', 'w')
    f.write(str(index_table))
    f.close()
    logging.info('Index {} is added'.format((str(index))))


#the oldest historical index is 2755
def createTable(start_index, end_index):
    index_table = {}
    for i in range(start_index,end_index+1):
        index_table[getFileDate(i)] = i
        f = open('indextable/indextable.txt','w')
        f.write(str(index_table))
        f.close()

