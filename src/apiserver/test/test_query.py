import logging
from pprint import pprint

from apiserver.model.pylang_enums import SOF
from config.flask_config_apiserver import db_pylang
from sql_db.pylang_model import Customer, Wallet, ObuCustomer, WalletCustomer, Obu

logger = logging.getLogger(__name__)

q = (db_pylang.session.query(Customer.id.label('customer_id'), Wallet.id.label('wallet_id'), (Customer.first_name + " " +
    Customer.last_name).label('customer_name'), Customer.phone_number.label('username')).join(ObuCustomer).join(Obu).
     join(WalletCustomer).join(Wallet).filter(Obu.serial_number_obu == "11AA22BB33CC4400").
     filter(WalletCustomer.default_sof_flag == SOF.DEFAULT)).all()

pprint(q)