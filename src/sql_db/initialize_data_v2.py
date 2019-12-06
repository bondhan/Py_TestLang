import logging
from pprint import pprint

from apiserver.model.pylang_enums import Status, SOF, OrganizationType, DefaultFlag, ReconFlag, IdentityType
from common.helper import HelperFunc
from customer_input.payment_test import getDateTime
from sql_db.pylang_model import Obu, ObuCustomer, Customer, Wallet, WalletCustomer, Organization, TransactionType, \
    OrganizationCommunication, TransactionSummary
from config.flask_config_apiserver import db_pylang, app_apiserver
from src.config.logging import LogConfig

log = LogConfig(__name__)
logger = log.create_logger()


if __name__ == '__main__':
    # create_logger the log

    # create_logger flask
    db_pylang.app = app_apiserver
    db_pylang.init_app(app_apiserver)
    db_pylang.create_all()

    num_records = 2
    num_dependant_obj = 2000
    num_owners = num_dependant_obj // num_records

    obus = []
    wallets = []
    customers = []
    cust_wallet = []
    orgs = []
    trans_type = []
    org_comms = []

    # create obu objects
    for number in range(1, num_dependant_obj + 1):
        obus.append(Obu(f"{number:016}", f"SN{number:014}", HelperFunc.getRandom(6, True), f"PT Angin Ribut {number}", 0))

    # create wallet objects
    for number in range(1, num_dependant_obj + 1):
        wallets.append(Wallet(f"WL{number:018}", f"{number*10000}"))

    # create customers
    for number in range(1, num_owners + 1):
        customers.append(Customer(f"081{number:011}", f"cust{number}@texo.id", f"cust{number}", f"omer{number}", "depok", "depok", "1234", "62", IdentityType.KTP.value, f"ID{number}", f"TAX{number}"))

    index = 0
    for cust in range(num_owners):
        for i in range(1,num_records+1):
            customers[cust].customer_obus.append(ObuCustomer(obus[index], i, Status.ACTIVE.value))
            index = index + 1

    index = 0
    for cust in range(num_owners):
        for i in range(1, num_records + 1):
            customers[cust].customer_wallets.append(WalletCustomer(wallets[index], i, "000", "001", "1", Status.ACTIVE.value, SOF.DEFAULT.value if (i % num_records == 1 ) else SOF.NOT_DEFAULT.value, wallets[index].initial_balance))
            index = index + 1

    # create organizations
    orgs.append(Organization("Bank BNI", OrganizationType.BANK.value))
    orgs.append(Organization("Non Bank", OrganizationType.OTHERS.value))

    # create transaction type
    trans_type.append(TransactionType(orgs[0], 1, 1, "abcd0000", 1, 1))
    trans_type.append(TransactionType(orgs[1], 1, 1, "abcd0000", 1, 1))

    # create organization communication
    org_comms.append(OrganizationCommunication(orgs[0], "0.0.0.0", "0.0.0.0", "TCPIP", "RAW", "AES", "RSA", "RSA", "RHSIA",
                                          DefaultFlag.DEFAULT.value))
    org_comms.append(OrganizationCommunication(orgs[0], "0.0.0.0", "0.0.0.0", "TCPIP", "RAW", "AES", "RSA", "RSA", "RHSIA",
                                          DefaultFlag.DEFAULT.value))

    for i in range(num_dependant_obj):
        db_pylang.session.add(obus[i])
        db_pylang.session.add(wallets[i])

    for i in range(num_owners):
        db_pylang.session.add(customers[i])

    for i in range(len(orgs)):
        db_pylang.session.add(orgs[i])

    for i in range(len(trans_type)):
        db_pylang.session.add(trans_type[i])

    for i in range(len(org_comms)):
        db_pylang.session.add(org_comms[i])

    db_pylang.session.commit()
    db_pylang.session.close()