import logging

from flask import jsonify

from sql_db.pylang_model import Customer
from config.flask_config_apiserver import db_pylang, ma_apiserver, app_apiserver


logger = logging.getLogger(__name__)

class CustomerSchema(ma_apiserver.ModelSchema):
    class Meta:
        model = Customer


@app_apiserver.route('/purchase')
def  index():
    cust_bondhan = Customer.query.filter_by(email_address = 'bondhan@texo.id').first()
    customer_schema = CustomerSchema()
    output = customer_schema.dump(cust_bondhan).data
    return jsonify(output)

@app_apiserver.route('/saldo')
def  showall():
    customers = Customer.query.all()
    customers_schema = CustomerSchema(many=True)
    output = customers_schema.dump(customers).data
    return jsonify(output)


if __name__ == '__main__':
    # create_logger the log
    logger = LogConfig().create_logger(__file__)

    # create_logger flask
    db_pylang.app = app_apiserver
    db_pylang.init_app(app_apiserver)
    app_apiserver.run()


