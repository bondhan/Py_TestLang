import os
import sys

sys.path.append(os.path.abspath('.\src'))
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
os.environ['PYTHONPATH'] = os.path.abspath('..') + ";" + os.path.abspath('.')

import uuid
import pika

from flask import request
from config.logging import LogConfig
from sql_db.pylang_model import TransactionType, TransactionSummary, WalletCustomer
from apiserver.model.constants import HTTP_ERROR_409_DATA_NOT_FOUND
from apiserver.model.pylang_enums import ReconFlag
from apiserver.schema.WalletCustomerSchema import WalletCustomerSchema
from common.responseencrypted import ResponsePlain
from config.flask_config_apiserver import DEBUG, db_pylang
from config.flask_config_isoclient import app_isoclient
from iso_client.schema.payment_isoclient_schema import PaymentIsoClientRequestSchema
from config.iso8583_config import queue_name
from iso8583.ISO8583 import *
from iso8583.ISOErrors import *

# create_logger the log
log = LogConfig(__file__)
logger = log.create_logger()

db_pylang.app = app_isoclient
db_pylang.init_app(app_isoclient)


class IsoMessageClient(object):
    def __init__(self):
        # init pika/rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        # self.result = self.channel.queue_declare(queue=queue_name, durable=True, no_ack=False, exclusive=True)
        self.result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = self.result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            # self.response = body.decode()
            self.response = body.decode()

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=message)

        while self.response is None:
            self.connection.process_data_events()

        return self.response

    def send_iso_message(self, payment_data):
        iso = ISO8583()
        iso.setMTI('0200')
        iso.setBit(3, '303000')
        iso.setBit(4, str(payment_data.trx_amount))
        iso.setBit(7, payment_data.transaction_date.strftime("%Y%m%d"))
        iso.setBit(11, payment_data.trace_number[0:6])
        iso.setBit(48, payment_data.username + payment_data.customer_name)
        iso.setBit(49, 'IDR')
        iso.setBit(103, payment_data.va_number)

        try:
            message = iso.getNetworkISO()
            logger.debug('Sending ... %s' % message)

            # message = "hello"
            resp = self.call(message)

            try:


                logger.debug("\nInput ASCII |%s|" % resp)
                isoAns = ISO8583()
                isoAns.setNetworkISO(self.response)
                v1 = isoAns.getBitsAndValues()

                for v in v1:
                    logger.debug('Bit %s of type %s with value = %s' % (v['bit'], v['type'], v['value']))

                if isoAns.getMTI() == '0210':
                    logger.debug("\tThat's great !!! The server understand my message !!!")
                else:
                    logger.debug("The server doesn't understand my message!")
                    raise ErrorResponseBit39("MTI is not 210")

                if isoAns.getBit(39) != '00':
                    raise ErrorResponseBit39(f"Bit 39 is not 00 but {isoAns.getBit(39)}")

            except InvalidIso8583 as ii:
                logger.debug(ii)
                raise Exception("InvalidIso8583")

        except Exception as ii:
            logger.debug(ii)
            raise Exception("Error Sending ISO8583")


class ErrorResponseBit39(Exception):
    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class IsoServerTimeout(Exception):
    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


@app_isoclient.route('/process_payment', methods=['POST'])
def process_payment():
    logger.debug("get the data from apiserver")
    data = request.get_json()

    logger.debug(f"data = {data}")
    payment_isoclient_req = PaymentIsoClientRequestSchema().load(data)
    payment_isoclient = payment_isoclient_req.data

    logger.debug("query to get the balance, so lock the row")
    wallet_cust = WalletCustomer.query.with_for_update().filter(
        WalletCustomer.wallet_id == payment_isoclient.obu_wallet_id).filter(
        WalletCustomer.customer_id == payment_isoclient.customer_id).first()

    logger.debug("check if wallet exist ( should be ok because api server already did query)")
    if wallet_cust is None:
        return ResponsePlain().get_response("102", "data not found",
                                            "data not found"), HTTP_ERROR_409_DATA_NOT_FOUND

    logger.debug("get the dictionary")
    wallet_customer_schema = WalletCustomerSchema()
    wallet_customer = wallet_customer_schema.dump(wallet_cust).data

    logger.debug('balance = ' + str(wallet_customer['balance']))

    logger.debug("test if balance is okay")
    trx_amount_num = int(payment_isoclient.trx_amount)

    logger.debug("check if balance is sufficient, if not then throw error message")
    if wallet_customer['balance'] < trx_amount_num:
        return ResponsePlain().get_response("000", "Error",
                                            f"ISOCLIENT, Insufficient Fund, fund available is {wallet_customer['balance']}"), 409

    try:
        isomsgclient = IsoMessageClient();
        isomsgclient.send_iso_message(payment_isoclient)
    except ValueToLarge:
        return ResponsePlain().get_response("999", "Error", "Value too large"), 500
    except BitInexistent:
        return ResponsePlain().get_response("999", "Error", "Bit not existent"), 500
    except InvalidValueType:
        return ResponsePlain().get_response("999", "Error", "Invalid value type"), 500
    except InvalidBitType:
        return ResponsePlain().get_response("999", "Error", "Invalid Bit Type"), 500
    except InvalidIso8583 as e:
        return ResponsePlain().get_response("999", "Error", f"Invalid Iso 8583 Reason: {e}"), 500
    except ErrorResponseBit39 as e:
        return ResponsePlain().get_response("999", "Error",
                                            f"ISOCLIENT: Insufficient Fund (Bit 39 not 00) Reason {e}"), 500
    except IsoServerTimeout:
        return ResponsePlain().get_response("999", "Error", "Cannot connect to ISO 8583 Server"), 500
    except Exception as e:
        return ResponsePlain().get_response("999", "Error", f"Internal Error msg = {e}"), 500

    logger.debug("get the new balance, and update the WalletCustomer")
    new_balance = wallet_customer['balance'] - trx_amount_num

    logger.debug("update the wallet")
    wallet_cust.balance = new_balance

    logger.debug("create the transaction detail")
    trans_type = TransactionType.query.filter(
        TransactionType.organization_id == payment_isoclient.organisation_id).first()
    trans_sum = TransactionSummary(trans_type, payment_isoclient.transaction_date, payment_isoclient.location,
                                   payment_isoclient.trx_amount, 0, payment_isoclient.trx_amount,
                                   ReconFlag.NO.value,
                                   payment_isoclient.trace_number, wallet_cust)

    logger.debug("insert to db")
    db_pylang.session.add(trans_sum)
    db_pylang.session.commit()

    return ResponsePlain().get_response("000", "success",
                                        f"ISOCLIENT: penarikan berhasil {payment_isoclient.location}"), 200


if __name__ == '__main__':
    app_isoclient.run(host='0.0.0.0', port='8080')
