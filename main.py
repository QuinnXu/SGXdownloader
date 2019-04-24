import logging
import sys, getopt
from dailyupdate import dailyUpdate, recreateIndextable
from retrieval import retrieval
from automation import automation
import configparser as cp


# set up logging config
logging.basicConfig(filename='logfile.log',
                    level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)



ERROR_DICT = {
    'CONFIG_ERROR': 'please check your config file.',
    'DATE_ERROR': 'please check date format',
    'INDEX_ERROR': 'please check date with indextable',
    'INIT_ERROR': 'pleas ask for support'
}


def printHelp():
    print(
    """
Usage: python3 main.py [OPTION]...

This program is a SGX Derivatives files downloader, which could work both automatically and manually.
Please read REEDME.md before use.

Mandatory arguments to long options are mandatory for short options too.
    -a, --automation
    -c, --config=FILE_NAME      Load config from FILE_NAME, default file is default.cfg
                                ........
    -h, --history=DATE          Download historical data. 
                                DATE could be one or several dates split by "," 
                                e.g. 20190329 for 29 March 2019.
                                e.g. 20190201,20190329 for two days.
                                Please notice that the date format should be YYYYMMDD.
    -i, --initializing          Crawling coordination of date& url index,
                                which is for downloading historical file.
                                Please do it when indextable is not exist or needs replacement.
    -u, --update                Download latest available files.
    -H, --help                  Print help information         
    """
    )



if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "aiuh:c:H",
                                   ['automation','initializing','update','history=','config=','help'])
        opd = dict(opts)
        if '-a' in opd:
            opd['--automation'] = opd['-a']
        if '-c' in opd:
            opd['--config'] = opd['-c']
        if '-h' in opd:
            opd['--history'] = opd['-h']
        if '-i' in opd:
            opd['--initializing'] = opd['-i']

        if '-H' in opd or '--help' in opd:
            printHelp()
        elif '-u' in opd or '--update' in opd:
            print('Download latest files')
            dailyUpdate()

        elif '--history' in opd:
            dates = opd['--history'].replace('=','').split(',')
            for i in dates:
                if len(i) == 8:
                    try:
                        retrieval(i)
                    except Exception as e:
                        logging.error('invalid date' + str(e))
                        print(ERROR_DICT['INDEX_ERROR'])
                else:
                    print(ERROR_DICT['DATE_ERROR'])
        elif '--automation' in opd:
            automation()

        elif '--initializing' in opd:
            try:
                recreateIndextable()
            except Exception as e:
                logging.error('indextable fail to create' + str(e))
                print(ERROR_DICT['INIT_ERROR'])

        if '--config' in opd:
            try:
                conf = cp.ConfigParser()
                if opd['--config'] == '':
                    opd['--config'] = 'default.cfg'
                conf.read(opd['--config'])
                print(conf.get('main', 'logging_level'))

            except Exception as e:
                logging.error('config setting' + str(e))
                print(ERROR_DICT['CONFIG_ERROR'])


    except Exception as e:
        printHelp()
        print(e)

