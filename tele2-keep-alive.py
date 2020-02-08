#!/usr/bin/env python
import sys
import xml.etree.cElementTree as eT
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class SMS:
    def __init__(self):
        self.message = ''
        self.send_to = []


class SendSMS:
    def __init__(self):
        self.URL = 'http://192.168.8.1/'  # the url for the dongle, this is usually http://192.168.8.1/
        self.default_page = self.URL + 'html/index.html'
        self.sms_sender_URL = self.URL + 'html/smsinbox.html'
        self.sms_send_url = self.URL + 'api/sms/send-sms'

        self.csrf_token_pattern = '<meta name="csrf_token" content="'
        self.csrf_token_name = "csrf_token"
        self.sms_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session = requests.Session()
        self.token = ''

    def send(self, sms):
        self.create_session()
        self.get_token()
        data = self.merge_template(sms)
        headers = dict()
        headers['__RequestVerificationToken'] = self.token
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Content-Type'] = 'text/xml'

        self.session.post(self.sms_send_url, data=data, headers=headers)

    def create_session(self):
        self.session.get(self.default_page)

    def get_token(self):
        # Huawei E3372: the CSRF token is in the HTML body inside a 'meta' element called 'csrf_token'. !!!
        # There are 2 of such tokens in the response, you must use the first one!!
        response = self.session.get(self.sms_sender_URL)
        if 'bs4' not in sys.modules:
            print('WARNING! HTML processing module BeautifulSoup is not available, '
                  'from this point onwards we can only guess where the csrf token is!')
            token_start = response.text.find(self.csrf_token_pattern)
            if token_start != -1:
                token_start += len(self.csrf_token_pattern)
                token_end = token_start + response.text[token_start:].find('"')
                self.token = response.text[token_start:token_end]

        else:
            soup = BeautifulSoup(response.text, "html.parser")
            for token in soup.findAll('meta', attrs={'name': self.csrf_token_name}):
                self.token = token['content']
                break

    def merge_template(self, sms):
        request = eT.Element("request")
        pageindex = eT.SubElement(request, "Index")
        pageindex.text = "-1"

        phones = eT.SubElement(request, "Phones")
        # sca = eT.SubElement(request, "Sca")
        content = eT.SubElement(request, "Content")
        length = eT.SubElement(request, "Length")
        reserved = eT.SubElement(request, "Reserved")
        reserved.text = "1"
        date = eT.SubElement(request, "Date")

        for number in sms.send_to:
            phone = eT.SubElement(phones, "Phone")
            phone.text = number

        content.text = sms.message
        length.text = str(len(sms.message))
        date.text = self.sms_time
        return eT.tostring(request, 'utf-8', method="xml")


def main():
    number = '1280'
    sms = SMS()
    sms.send_to.append(number)
    sms.message = '1GB EXTRA'

    sms_sender = SendSMS()
    sms_sender.send(sms)
    print('Send!')


def loop():
    minutes = 10
    from time import sleep
    while True:
        try:
            main()
        except requests.exceptions.ConnectionError:
            pass
        print('Sleeping %d minutes...' % minutes)
        sleep(60 * minutes)


if __name__ == '__main__':
    loop()
