import logging

from sql_db.pylang_model import WalletCustomer
from config.flask_config_apiserver import ma_apiserver

logger = logging.getLogger(__name__)

class WalletCustomerSchema(ma_apiserver.ModelSchema):
    class Meta:
        model = WalletCustomer

