from config.flask_config_apiserver import db_pylang
from config.logging import LogConfig
from sql_db.pylang_model import Organization, TransactionType, OrganizationCommunication, TransactionSummary
from apiserver.model.pylang_enums import OrganizationType, ReconFlag, DefaultFlag
from common.helper import HelperFunc
from config.flask_config_isoclient import app_isoclient

if __name__ == '__main__':
    # create_logger the log
    logger = LogConfig().create_logger(__file__)

    # create_logger flask
    db_pylang.app = app_isoclient
    db_pylang.init_app(app_isoclient)
    db_pylang.create_all()

    org1 = Organization("Bank BNI", OrganizationType.BANK.value)
    org2 = Organization("Koperasi", OrganizationType.OTHERS.value)

    trans_type1 = TransactionType(org1, 1, 1, "abcd0000", 1, 1)
    trans_type2 = TransactionType(org2, 1, 1, "abcd1234", 1, 1)

    org_comm1 = OrganizationCommunication(org1, "0.0.0.0", "0.0.0.0", "TCPIP", "RAW", "AES", "RSA", "RSA", "RHSIA", DefaultFlag.DEFAULT.value)
    org_comm2 = OrganizationCommunication(org2, "0.0.0.0", "0.0.0.0", "TCPIP", "RAW", "AES", "RSA", "RSA", "RHSIA", DefaultFlag.DEFAULT.value)

    trans_sum1 = TransactionSummary(trans_type1, HelperFunc.getDateTime(), "Jakarta", 1000, 2000, 3000, ReconFlag.NO.value, "1122334545")
    trans_sum2 = TransactionSummary(trans_type2, HelperFunc.getDateTime(), "Depok", 1000, 2000, 3000, ReconFlag.NO.value, "112233445566")

    db_pylang.session.add_all([org1, org2])
    db_pylang.session.add_all([trans_type1, trans_type2])
    db_pylang.session.add_all([org_comm1, org_comm2])
    db_pylang.session.add_all([trans_sum1, trans_sum2])
    db_pylang.session.commit()
    db_pylang.session.close()