import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apiserver.model.base import Base
from sql_db.pylang_model import Customer, Wallet

logger = logging.getLogger(__name__)

engine = create_engine('mysql+mysqldb://root@localhost:3306/pylang_db')
Session = sessionmaker(bind=engine)
session = Session()
session._model_changes = {}

Base.metadata.create_all(engine)


wallets = session.query(Wallet)

for row in wallets:
    print(row.wallet_account_no + " " + str(row.initial_balance) + " " + str(row.created_datetime) + " " + str(row.updated_datetime))


wallets_bondhan = session.query(Customer)#.filter_by(email_address = 'bondhan@texo.id')


for row in wallets_bondhan:
    print(row.phone_number + " " + row.email_address + " " + row.first_name + " " + row.last_name)


session.close()