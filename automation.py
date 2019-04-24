import logging
import schedule
import time
import sys
from dailyupdate import dailyUpdate


def automation():
    print('automation start!')
    schedule.every().day.at("08:00").do(dailyUpdate)
    while True:
        try:
            schedule.run_pending()
            sys.stdout.write('\r')
            sys.stdout.write('automation standby .')
            time.sleep(1)
            sys.stdout.write('\r')
            sys.stdout.write('automation standby ..')
            time.sleep(1)
            sys.stdout.write('\r')
            sys.stdout.write('automation standby ...')
            time.sleep(1)
            sys.stdout.write('\r')
            time.sleep(1)
        except Exception as e:
            logging.error(str(e) + 'automation failed!')
