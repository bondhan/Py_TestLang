import logging

from apiserver.model.pylang_enums import Status, SOF, OrganizationType, DefaultFlag, ReconFlag
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

    # create obu objects
    obu0 = Obu("1111000011110000", "1111000011110000", "1234234324324", "PT Angin Ribut", 0)
    obu1 = Obu("1111000011110001", "1111000011110001", "1234234324324", "PT Angin Ribut", 0)
    obu2 = Obu("1111000011110002", "1111000011110002", "1234234324324", "PT Angin Ribut", 0)
    obu3 = Obu("1111000011110003", "1111000011110003", "1234234324324", "PT Angin Ribut", 0)
    obu4 = Obu("1111000011110004", "1111000011110004", "1234234324324", "PT Angin Ribut", 0)

    # create wallets
    wallet0 = Wallet("1234567890", "9999999")
    wallet1 = Wallet("1234567891", "9999999")
    wallet2 = Wallet("1234567892", "9999")
    wallet3 = Wallet("1234567893", "5000")

    # create customers

    cust_bondhan = Customer("11223344", "bondhan@texo.id", "bondhan", "novandy", "depok", "depok", "1234", "62", "0",
                            "92749832743asa9", "1234")
    cust_meli = Customer("7789966", "meli@texo.id", "meli", "meli", "depok", "depok", "1234", "62", "0",
                         "92749832743asa9", "1234")


    # create_logger customer bondhan with obus and wallets
    cust_bondhan.customer_obus.append(ObuCustomer(obu0, 1, Status.ACTIVE.value))
    cust_bondhan.customer_obus.append(ObuCustomer(obu1, 2, Status.ACTIVE.value))

    cust_wallet1 = WalletCustomer(wallet0, 1, "000", "001", "1", Status.ACTIVE.value, SOF.DEFAULT.value, wallet0.initial_balance)
    cust_wallet2 = WalletCustomer(wallet1, 2, "000", "001", "1", Status.ACTIVE.value, SOF.NOT_DEFAULT.value, wallet1.initial_balance)

    cust_bondhan.customer_wallets.append(cust_wallet1)
    cust_bondhan.customer_wallets.append(cust_wallet2)

    # create_logger customer meli with obus and wallets
    cust_meli.customer_obus.append(ObuCustomer(obu2, 1, Status.ACTIVE.value))
    cust_meli.customer_obus.append(ObuCustomer(obu3, 2, Status.ACTIVE.value))
    cust_meli.customer_wallets.append(
        WalletCustomer(wallet2, 1, "000", "001", "1", Status.ACTIVE.value, SOF.DEFAULT.value, wallet0.initial_balance))
    cust_meli.customer_wallets.append(
        WalletCustomer(wallet3, 2, "000", "001", "1", Status.ACTIVE.value, SOF.NOT_DEFAULT.value,
                       wallet1.initial_balance))

    # create organization
    org1 = Organization("Bank BNI", OrganizationType.BANK.value)
    org2 = Organization("Koperasi", OrganizationType.OTHERS.value)

    # create transaction type
    trans_type1 = TransactionType(org1, 1, 1, "abcd0000", 1, 1)
    trans_type2 = TransactionType(org2, 1, 1, "abcd1234", 1, 1)

    # create organization communication
    org_comm1 = OrganizationCommunication(org1, "0.0.0.0", "0.0.0.0", "TCPIP", "RAW", "AES", "RSA", "RSA", "RHSIA",
                                          DefaultFlag.DEFAULT.value)
    org_comm2 = OrganizationCommunication(org2, "0.0.0.0", "0.0.0.0", "TCPIP", "RAW", "AES", "RSA", "RSA", "RHSIA",
                                          DefaultFlag.DEFAULT.value)

    #create transaction summary
    trans_sum1 = TransactionSummary(trans_type1, getDateTime(), "Jakarta", 1000, 2000, 3000, ReconFlag.NO.value,
                                    "1122334545", cust_wallet1)
    trans_sum2 = TransactionSummary(trans_type2, getDateTime(), "Depok", 1000, 2000, 3000, ReconFlag.NO.value,
                                    "112233445566", cust_wallet2)

    db_pylang.session.add_all([org1, org2])
    db_pylang.session.add_all([trans_type1, trans_type2])
    db_pylang.session.add_all([org_comm1, org_comm2])
    db_pylang.session.add_all([trans_sum1, trans_sum2])

    db_pylang.session.add_all([obu0, obu1, obu2, obu3, obu4])
    db_pylang.session.add_all([wallet0, wallet1, wallet2, wallet3])
    db_pylang.session.add(cust_bondhan)
    db_pylang.session.add(cust_meli)
    db_pylang.session.commit()
    db_pylang.session.close()