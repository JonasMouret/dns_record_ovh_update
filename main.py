import ovh
import urllib.request
import logging
import os
from dotenv import load_dotenv
from datetime import datetime


def get_external_ip():
    return urllib.request.urlopen('https://ident.me').read().decode('utf8')

def main():
    now = datetime.now()
    logging.info(f'STARTING AT {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
    logging.info('=============== Loading env var ===============')
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    API_ENDPOINT = os.getenv('API_ENDPOINT')
    logging.info('DONE\n')
    domain = 'mobo-server.ovh'
    subdomain = None
    ip = get_external_ip()
    logging.info('=============== Starting ovh client ===============')
    client = ovh.Client(
        endpoint=API_ENDPOINT,
        application_key=API_KEY,
        application_secret=API_SECRET,
        consumer_key=CONSUMER_KEY,
    )
    logging.info('DONE\n')
    logging.info('=============== Getting domain records ===============')
    records = client.get('/domain/zone/{}/record'.format(domain), fieldType='AAAA')
    logging.info('DONE\n')
 
    for record in records:
        logging.info('=============== Getting record ===============')
        dns_record = client.get('/domain/zone/{}/record/{}'.format(domain, record))
        logging.info('DONE\n')

        dns_record_ip = dns_record.get('target')
        logging.info(f'==> IP from DNS record: {dns_record_ip} <==\n')
        logging.info('=============== Checking record ===============')
        if dns_record_ip != ip:
            logging.info('Updating record {} from {} to {}\n'.format(record, dns_record_ip, ip))
            response = client.put('/domain/zone/{}/record/{}'.format(domain, record), target=ip)
        else:
            logging.info('No need to update record\n')
    logging.info(f'END AT {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    return True

if __name__ == '__main__':
    logging.basicConfig(filename="log_dns_records.log", level=logging.INFO)
    load_dotenv()
    main()