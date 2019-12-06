import os
import sys

sys.path.append(os.path.abspath('.\src'))
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
os.environ['PYTHONPATH'] = os.path.abspath('..') + ";" + os.path.abspath('.')

import json
import pprint
import sys, getopt, time
import requests
from random import randint
from flask_marshmallow import Schema
from flask_marshmallow.fields import  fields
from marshmallow import post_load
from config.cryto_data import secret_key
from config.logging import LogConfig
from crypto.aes_ecb_base64 import AesEcbBase64

# create_logger the log
log = LogConfig(__file__)
logger = log.create_logger()

#change below if needed
debug = True

# url = "https://etc.texo.id"
# url = "http://localhost:5000"
url = "http://192.168.108.3:5000"

# change this if needed
api_payment = "/payment"

def usage():
    print('\tusage:')
    print('\t\tpayment [-g org_id] [-o obu_serial_number] [-r trx_type_id] [-a trx_amount] [-l location] [-d description] [-t trace_number]')

def getRandom(digit, withZero):
    randomNum = ''

    for i in range(digit):
        randomNum = randomNum + str(randint(0 if withZero else 1, 9))

    return randomNum

def getDateTime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def getDateTimeIso():
    u = time.strftime("%z")
    utc = u[:3] + ":" + u[-2:]
    return time.strftime("%Y-%m-%dT%H:%M:%S") + utc

def sendJsonData(url, payload):
    head = {'content-type': 'application/json'}
    return requests.post(url, data=payload, headers=head)



class GenericResponse(object):
    def __init__(self, organisation_id, response):
        self.organisation_id = organisation_id
        self.response = response


class GenericRequestSchemaLocal(Schema):
    class Meta:
        strict = True

    organisation_id = fields.Str()
    response = fields.Str()

    @post_load
    def get_request(self, data):
        return GenericResponse(**data)


def sendPurchase(obu_serial_number, trx_type_id, trx_amount, location, description, trace_number, organization_id):
    if (debug):
        print()
        print("Composing and Sending post message...")

    # compose message
    plain = "{\n" \
        + "	\"obu_serial_number\":\"" + obu_serial_number + "\",\n" \
        + "	\"trx_type_id\":\"" + trx_type_id + "\",\n" \
        + "	\"trx_amount\":\"" + trx_amount+ "\",\n" \
        + "	\"location\":\"" + location + "\",\n" \
        + "	\"transaction_date\":\"" + getDateTime()+ "\",\n" \
        + "	\"description\": \"" + description + "\",\n" \
        + "	\"trace_number\": \"" + trace_number + "\"\n" \
        + "}";

    if (debug):
        print(plain)

    aesecb = AesEcbBase64(secret_key)
    encrypted = aesecb.do_encrypt(plain)

    if (debug):
        print("encrypted data " + encrypted)

    json_data = "{\"organisation_id\":\""+organization_id+"\",\"data\":\"" + encrypted + "\"}";

    print(f"Send encrypted data: \n {json_data}")

    resp = sendJsonData(url + api_payment, json_data)

    print(f"\nGot Response with status_code = {resp.status_code}")
    print("Received Msg:")
    pprint.pprint(resp.json())

    generic_req = GenericRequestSchemaLocal().load(resp.json())
    generic = generic_req.data

    decrypted = aesecb.do_decrypt(generic.response)
    print("\nDecrypted Msg = ")
    pprint.pprint(json.loads(decrypted))
    print("\n")

def main(argv):
    #getopt variable
    obu_serial_number = ''
    trx_type_id = ''
    trx_amount = ''
    location = ''
    description = ''
    trace_number = ''
    organization_id = ''

    # get the parameter
    try:
        opts, args = getopt.getopt(argv, 'g:o:r:a:l:d:t:')

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-o':
            obu_serial_number = arg
        elif opt in ("-r"):
            trx_type_id = arg
        elif opt in ("-a"):
            trx_amount = arg
        elif opt in ("-l"):
            location = arg
        elif opt in ("-d"):
            description = arg
        elif opt in ("-t"):
            trace_number = arg
        elif opt in ("-g"):
            organization_id = arg

    # do parameter check

    if obu_serial_number == '' or trx_type_id == '' or trx_amount == '' or location == '' or  description == '' or  trace_number == '' or  organization_id == '':
        usage()
        sys.exit(2)

    sendPurchase(obu_serial_number, trx_type_id, trx_amount, location, description, trace_number, organization_id)

if __name__ == "__main__":
    # main(sys.argv[1:])
    sendPurchase("1111000011110033", "001", "1000", "Pintu Tol Jor", "Pembayaran tol golongan 1", getRandom(12, False),
                 "999") # return no organization found

    sendPurchase("1111000011110033", "001", "1000", "Pintu Tol Jor", "Pembayaran tol golongan 1", getRandom(12, False),
                 "001") # no data found

    sendPurchase("1111000011110001", "001", "9999999.99", "Pintu Tol Jor", "Pembayaran tol golongan 1", getRandom(12, False),
                 "001") # insufficient balance

    sendPurchase("1111000011110099", "001", "1000", "Pintu Tol Jor", "Pembayaran tol golongan 1", getRandom(12, False),
                 "001") #

    #berhasil
    sendPurchase("1111000011110000", "001", "1000", "Pintu Tol Jor", "Pembayaran tol golongan 1", getRandom(12, False), "001")
    sendPurchase("1111000011110000", "001", "1000", "Pintu Tol Jor", "Pembayaran tol golongan 1", getRandom(12, False),
                 "001")
