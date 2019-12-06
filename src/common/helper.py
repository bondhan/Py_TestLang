import logging
import time
from random import randint
import requests


logger = logging.getLogger(__name__)

class HelperFunc:
    @staticmethod
    def getRandom(digit, withZero):
        randomNum = ''

        for i in range(digit):
            randomNum = randomNum + str(randint(0 if withZero else 1, 9))

        return randomNum

    @staticmethod
    def getDateTime():
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getDateTimeIso():
        u = time.strftime("%z")
        utc = u[:3] + ":" + u[-2:]
        return time.strftime("%Y-%m-%dT%H:%M:%S") + utc

    @staticmethod
    def sendJsonData(url, payload):
        head = {'content-type': 'application/json'}
        resp = requests.post(url, data=payload, headers=head, timeout=10)

        return resp

