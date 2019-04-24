import os, sys, time, requests
import logging

logging.basicConfig(filename='logfile.log', level=logging.INFO)


#progress record
def chunkReport(bytes_so_far, total_size, filename):
    percent = float(bytes_so_far) / total_size
    percent = round(percent * 100, 2)
    sys.stdout.write('\r')
    sys.stdout.write(filename + " Downloaded {} of {} bytes {}%".format(bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
        sys.stdout.write('\n')


def downloader(date, index):
    logging.info('Downloading {} files'.format(date))
    data_dir = './files/' + str(date)
    if not os.path.exists(path=data_dir):
        os.mkdir(path=data_dir, mode=0o777)
    datatypes = ['TC.txt', 'TickData_structure.dat', 'TC_structure.dat', 'WEBPXTICK_DT.zip']
    for datatype in datatypes:
        try:
            url = 'https://links.sgx.com/1.0.0/derivatives-historical/' + str(index) + '/' + datatype

            r = requests.get(url, stream=True)
            content_size = int(r.headers['content-length'])
            chunk_size = 65536
            bytes_so_far = 0

            if datatype == 'WEBPXTICK_DT.zip':
                filename = 'WEBPXTICK_DT-' + str(date) + '.zip'
            elif datatype == 'TC.txt':
                filename = 'TC_' + str(date) + '.txt'
            else:
                filename = datatype
            f = open(data_dir + '/' + filename, "wb")

            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bytes_so_far += len(chunk)
                    chunkReport(bytes_so_far, content_size, filename)

            f.close()

        except Exception as e:
            logging.warning('{} download failed '.format(str(date)) + str(e))
            # record failed file index
            r = open('indextable/recovery.txt', 'a')
            r.write(str(date) + ',')
            r.close()
