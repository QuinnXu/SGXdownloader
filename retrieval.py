from downloader import downloader
import logging

#download files by indextable retreval
def retrieval(date):
    f = open('indextable/indextable.txt', 'r')
    a = f.read()
    index_table = eval(a)
    f.close()

    try:
        downloader(date, index_table[str(date)])
        return
    except Exception as e:
        logging.error(str(date)+' is not in indextable, please check '+str(e))
