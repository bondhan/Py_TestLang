import os
import sys
import threading
from queue import Queue

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
from flask_marshmallow.fields import fields
from marshmallow import post_load
from config.cryto_data import secret_key
from config.logging import LogConfig
from crypto.aes_ecb_base64 import AesEcbBase64
from apiserver.model.pylang_enums import SOF
from apiserver.schema.payment import PaymentSchema
from config.flask_config_apiserver import db_pylang
from sql_db.pylang_model import Customer, Wallet, WalletCustomer, ObuCustomer, Obu

# create_logger the log
log = LogConfig(__file__)
logger = log.create_logger()

# change below if needed
debug = True

# url = "https://etc.texo.id"
# url = "http://192.168.108.3:5000"
url = "http://127.0.0.1:5000"
# url = "https://dev-python.texo.id"

# change this if needed
api_payment = "/payment"

organization_id = '001'

def usage():
    print('\tusage:')
    print(
        '\t\tpayment [-g org_id] [-o obu_serial_number] [-r trx_type_id] [-a trx_amount] [-l location] [-d description] [-t trace_number]')


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

    organisation_id = fields.Str(required=True)
    response = fields.Str(required=True)

    @post_load
    def get_request(self, data):
        return GenericResponse(**data)


# def sendPurchase(obu_serial_number, trx_type_id, trx_amount, location, description, trace_number, organization_id):

def sendPurchase(q):
    global obu_list
    global gagal_list
    global berhasil_list

    while True:
        data = q.get()
        obu_serial_number = data[0]
        trx_type_id = data[1]
        trx_amount = data[2]
        location = data[3]
        description = data[4]
        trace_number = data[5]

        if debug:
            print()
            print("Composing and Sending post message...")

        # compose message
        plain = "{\n" \
                + "	\"obu_serial_number\":\"" + obu_serial_number + "\",\n" \
                + "	\"trx_type_id\":\"" + trx_type_id + "\",\n" \
                + "	\"trx_amount\":\"" + trx_amount + "\",\n" \
                + "	\"location\":\"" + location + "\",\n" \
                + "	\"transaction_date\":\"" + getDateTime() + "\",\n" \
                + "	\"description\": \"" + description + "\",\n" \
                + "	\"trace_number\": \"" + trace_number + "\"\n" \
                + "}";

        if debug:
            print(plain)

        aesecb = AesEcbBase64(secret_key)
        encrypted = aesecb.do_encrypt(plain)

        if debug:
            print("encrypted data " + encrypted)

        json_data = "{\"organisation_id\":\"" + organization_id + "\",\"data\":\"" + encrypted + "\"}";

        if debug:
            print(f"Send encrypted data: \n {json_data}")

        resp = sendJsonData(url + api_payment, json_data)

        if debug:
            print(f"\nGot Response with status_code = {resp.status_code}")
            print("Received Msg:")
            pprint.pprint(resp.json())

        generic_req = GenericRequestSchemaLocal().load(resp.json())
        generic = generic_req.data

        global result
        decrypted = aesecb.do_decrypt(generic.response)
        result = json.loads(decrypted)
        if debug:
            print("\nDecrypted Msg = ")
            pprint.pprint(result)
            print("\n")

        if resp.status_code == 200:
            berhasil_list.append(obu_serial_number)
        else:
            gagal_list.append(
                obu_serial_number + f" HTTP RESP = {resp.status_code}" + " - " + result['RC'] + " - " + result[
                    'message'] + " - " + result['description'])

        q.task_done()
        obu_list.append(obu_serial_number)


def main(argv):
    # getopt variable
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
    if obu_serial_number == '' or trx_type_id == '' or trx_amount == '' or location == '' or description == '' or trace_number == '' or organization_id == '':
        usage()
        sys.exit(2)

    sendPurchase(obu_serial_number, trx_type_id, trx_amount, location, description, trace_number, organization_id)


if __name__ == "__main__":
    # main(sys.argv[1:])
    purchases = []
    purchases_db = []
    obu_list = []
    gagal_list = []
    berhasil_list = []

    manyusers = True
    number_req = 1000
    # num_thread = number_req // 2
    num_thread = 50

    q = Queue()

    for i in range(num_thread):
        t = threading.Thread(target=sendPurchase, args=(q,))
        t.setDaemon(True)
        t.start()

    start = time.time()

    for i in range(1, number_req + 1, 1):
        print(f"putting {i}")

        if manyusers == True:
            data = (f"SN{i:014}", "001", "1.00", f"Gate {i}", f"Ini untuk cust ke {i}", getRandom(12, False), "001")
        else:
            data = ("SN00000000000001", "001", "1.00", "Gate 1", "Ini untuk cust ke 1", getRandom(12, False), "001")

        purchases.append(data)

        # result_sof = db_pylang.session.query(Customer.id.label('customer_id'), Wallet.id.label('wallet_id'),
        #                                      (Customer.first_name + " " + Customer.last_name).label('customer_name'),
        #                                      Customer.phone_number.label('username'),
        #                                      WalletCustomer.balance.label('balance')).join(ObuCustomer).join(Obu).join(
        #     WalletCustomer).join(Wallet).filter(
        #     Obu.serial_number_obu == f"SN{i:014}").filter(
        #     WalletCustomer.default_sof_flag == SOF.DEFAULT).first()
        #
        # purchase_schema = PaymentSchema()
        # payment_data = purchase_schema.dump(result_sof).data
        #
        # db_data = (f"SN{i:014}", f"{payment_data['customer_id']}", f"{payment_data['wallet_id']}",
        #            f"{payment_data['customer_name']}", f"{payment_data['username']}", f"{payment_data['balance']}")
        # purchases_db.append(db_data)

        q.put(data)

    print('Main thread waiting')
    q.join()
    finish = (time.time() - start)

    # print("purchases = ")
    # for purchase in purchases:
    #     print(*purchase)
    #
    # print("\npurchases_db = ")
    # for purchase in purchases_db:
    #     print(*purchase)

    print("Gagal = ")
    for gagal in gagal_list:
        print(gagal)

    print("Berhasil = ")
    print(*berhasil_list)

    print(f'Done in {finish} seconds')
    print(f"Total test = {len(obu_list)} gagal = {len(gagal_list)} berhasil = {len(berhasil_list)}")
