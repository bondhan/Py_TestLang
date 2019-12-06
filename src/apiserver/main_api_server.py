import os
import sys

from marshmallow import ValidationError

sys.path.append(os.path.abspath('.\src'))
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
os.environ['PYTHONPATH'] = os.path.abspath('..') + ";" + os.path.abspath('.')

import json
import requests
from flask import request
from common.responseencrypted import ResponseEncrypted, ResponseHeader, ResponsePlain
from apiserver.model.constants import HTTP_ERROR_409_DATA_NOT_FOUND, HTTP_ERROR_500, HTTP_ERROR_400_DATA_INCOMPLETE
from apiserver.schema.generic import GenericRequestSchema
from apiserver.schema.payment import PaymentRequestSchema, PaymentData
from config.cryto_data import secret_key
from config.flask_config_apiserver import db_pylang, app_apiserver
from config.flask_config_isoclient import iso_client_host, iso_client_payment
from sql_db.pylang_model import Wallet, Customer, ObuCustomer, Obu, WalletCustomer, Organization
from apiserver.model.pylang_enums import SOF
from apiserver.schema.payment import PaymentSchema
from crypto.aes_ecb_base64 import AesEcbBase64
from common.helper import HelperFunc
from config.logging import LogConfig

# create_logger the log
log = LogConfig(__file__)
logger = log.create_logger()

# attach the appi server to database
db_pylang.app = app_apiserver
db_pylang.init_app(app_apiserver)


@app_apiserver.route('/ping', methods=['POST'])
def pong():
    return ResponsePlain().get_response("000", "OK", "Pong"), 200

@app_apiserver.route('/payment', methods=['POST'])
def payment():
    logger.debug(request.get_json())

    logger.debug("Get the json request and deserialize it to an object")
    try:
        generic_req = GenericRequestSchema().load(request.get_json())
        generic = generic_req.data
    except ValidationError:
        return ResponsePlain().get_response("101", "Invalid data",
                                            "Wrong data or data incomplete"), HTTP_ERROR_400_DATA_INCOMPLETE
    except Exception:
        return ResponsePlain().get_response("999", "Invalid data",
                                            "Your data is no recognized"), HTTP_ERROR_400_DATA_INCOMPLETE

    try:
        logger.debug("Decrypt the data")
        aesecb = AesEcbBase64(secret_key)
        plain = aesecb.do_decrypt(generic.data)

        logger.debug(plain)
        logger.debug(type(plain))
        logger.debug(json.loads(plain))
    except Exception:
        return ResponsePlain().get_response("101", "invalid data",
                                            "fail decipher data, check if key is correct"), HTTP_ERROR_409_DATA_NOT_FOUND

    try:
        logger.debug("Unmarshal it from json to object")
        payment_request = PaymentRequestSchema().load(json.loads(plain))
        payment = payment_request.data
        logger.debug(payment.obu_serial_number)
    except ValidationError:
        return ResponseEncrypted().get_response(generic.organisation_id, "101", "Invalid data",
                                                "Wrong data or data incomplete"), HTTP_ERROR_400_DATA_INCOMPLETE
    except Exception:
        return ResponseEncrypted().get_response(generic.organisation_id, "101", "invalid data",
                                                "Invalid Parameter"), HTTP_ERROR_409_DATA_NOT_FOUND

    try:
        org = Organization.query.filter(Organization.id == generic.organisation_id).first()
        if org is None:
            return ResponseEncrypted().get_response(generic.organisation_id, "102", "Data Not Found",
                                                    f"Organization {generic.organisation_id} not found "), HTTP_ERROR_409_DATA_NOT_FOUND

        logger.debug("Query to db if data exist WITHOUT default SOF")
        result_without_sof = (db_pylang.session.query(Customer.id.label('customer_id'), Wallet.id.label('wallet_id'),
                                                      (Customer.first_name + " " + Customer.last_name).label(
                                                          'customer_name'), Customer.phone_number.label('username'),
                                                      WalletCustomer.balance.label('balance')).
            join(ObuCustomer).join(Obu).join(WalletCustomer).join(Wallet).filter(
            Obu.serial_number_obu == payment.obu_serial_number)).first()

        logger.debug("Check if data exist based on serial_number_obu and default SOF")
        if (result_without_sof is None):
            return ResponseEncrypted().get_response(generic.organisation_id, "102", "data not found",
                                                    f"Data with Obu = {payment.obu_serial_number} not found"), HTTP_ERROR_409_DATA_NOT_FOUND

        result_sof = (db_pylang.session.query(Customer.id.label('customer_id'), Wallet.id.label('wallet_id'),
                                              (Customer.first_name + " " + Customer.last_name).label('customer_name'),
                                              Customer.phone_number.label('username'),
                                              WalletCustomer.balance.label('balance')).
            join(ObuCustomer).join(Obu).join(WalletCustomer).join(Wallet).filter(
            Obu.serial_number_obu == payment.obu_serial_number)).filter(
            WalletCustomer.default_sof_flag == SOF.DEFAULT).first()

        logger.debug("Check if no data with active sof")
        if (result_sof is None):
            return ResponseEncrypted().get_response(generic.organisation_id, "103", "data not found",
                                                    "data not found"), HTTP_ERROR_409_DATA_NOT_FOUND

        purchase_schema = PaymentSchema()
        payment_data = purchase_schema.dump(result_sof).data

        logger.debug("Check if balance is sufficient")
        if (payment_data['balance'] < float(payment.trx_amount)):
            return ResponseEncrypted().get_response(generic.organisation_id, "104", "insufficient balance",
                                                    f"APISERVER: insufficient balance ({payment_data['balance']})"), HTTP_ERROR_409_DATA_NOT_FOUND

        plain = "{\n" \
                + "	\"organisation_id\":\"" + generic.organisation_id + "\",\n" \
                + "	\"trx_type_id\":\"" + payment.trx_type_id + "\",\n" \
                + "	\"trx_amount\":\"" + payment.trx_amount + "\",\n" \
                + "	\"va_number\":\"" + "11223344" + "\",\n" \
                + "	\"location\":\"" + payment.location + "\",\n" \
                + "	\"transaction_date\":\"" + payment.transaction_date + "\",\n" \
                + "	\"description\": \"" + payment.description + "\",\n" \
                + "	\"trace_number\": \"" + payment.trace_number + "\",\n" \
                + "	\"username\": \"" + payment_data['username'] + "\",\n" \
                + "	\"customer_name\": \"" + payment_data['customer_name'] + "\",\n" \
                + "	\"obu_wallet_id\": \"" + str(payment_data['wallet_id']) + "\",\n" \
                + "	\"customer_id\": \"" + str(payment_data['customer_id']) + "\"\n" \
                + "}";

        msg = json.loads(plain)
        load = json.dumps(msg)
    except Exception:
        return ResponseEncrypted().get_response(generic.organisation_id, "999", "Error Sever",
                                                "Something happen in api server"), HTTP_ERROR_500

    logger.debug("Send to isoclient the json message")

    try:
        resp = HelperFunc.sendJsonData(iso_client_host + iso_client_payment, load)
        status_code = resp.status_code
    except requests.exceptions.Timeout:
        return ResponseEncrypted().get_response(generic.organisation_id, "999", "Timeout",
                                                "Timeout Connecting to IsoClient"), HTTP_ERROR_500
    except Exception:
        return ResponseEncrypted().get_response(generic.organisation_id, "999", "Fail Connection",
                                                "Cannot connect to ISO Client"), HTTP_ERROR_500
    # return resp
    return ResponseHeader().get_response(generic.organisation_id, json.dumps(resp.json())), status_code


if __name__ == '__main__':
    app_apiserver.run(host='0.0.0.0')
