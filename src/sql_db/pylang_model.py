import logging

from sqlalchemy import Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship

from apiserver.model.pylang_enums import Status, SOF, IdentityType, DefaultFlag, OrganizationType, ReconFlag
from config.flask_config_apiserver import db_pylang

logger = logging.getLogger(__name__)

class Customer(db_pylang.Model):
    __tablename__ = "m_customer"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    phone_number = db_pylang.Column(db_pylang.String, index=True)
    email_address = db_pylang.Column(db_pylang.String, nullable=False)
    first_name = db_pylang.Column(db_pylang.String, nullable=False)
    last_name = db_pylang.Column(db_pylang.String, nullable=False)
    address = db_pylang.Column(db_pylang.String, nullable=False)
    city_code = db_pylang.Column(db_pylang.String, nullable=False)
    postal_code = db_pylang.Column(db_pylang.String, nullable=False)
    country_code = db_pylang.Column(db_pylang.String, nullable=False)
    identity_type = db_pylang.Column(db_pylang.Enum(IdentityType), nullable=False)
    identity_number = db_pylang.Column(db_pylang.String, nullable=False)
    tax_code = db_pylang.Column(db_pylang.String, nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), nullable=False)   #db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime  = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(), nullable=False)        #will be updated everytime there is update to this table

    customer_obus = db_pylang.relationship("ObuCustomer", cascade="all, delete-orphan", backref='m_customer')
    obus = association_proxy("customer_obus", "m_obu")

    customer_wallets = db_pylang.relationship("WalletCustomer", cascade="all, delete-orphan", backref='m_customer')
    wallets = association_proxy("cutomer_wallets", "m_wallet")

    def __init__(self, phone_number, email_address, first_name, last_name, address, city_code, postal_code, country_code, identity_type, identity_number, tax_code):
        self.phone_number = phone_number
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city_code = city_code
        self.postal_code = postal_code
        self.country_code = country_code
        self.identity_type = identity_type
        self.identity_number = identity_number
        self.tax_code = tax_code

class Obu(db_pylang.Model):
    __tablename__ = "m_obu"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    obu_id = db_pylang.Column(db_pylang.String, nullable=False)
    serial_number_obu = db_pylang.Column(db_pylang.String, nullable=False)
    aes_token_code = db_pylang.Column(db_pylang.String, nullable=False)
    obu_manufacturer = db_pylang.Column(db_pylang.String, nullable=False)
    initial_balance = db_pylang.Column(db_pylang.Numeric, nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), nullable=False)   #db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime  = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(), nullable=False)        #will be updated everytime there is update to this table

    def __init__(self, obu_id, serial_number_obu, aes_token_code, obu_manufacturer, initial_balance):
        self.obu_id = obu_id
        self.serial_number_obu = serial_number_obu
        self.aes_token_code = aes_token_code
        self.obu_manufacturer = obu_manufacturer
        self.initial_balance = initial_balance


class ObuCustomer(db_pylang.Model):
    __tablename__ = "m_obu_customer"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, nullable=False, autoincrement=True)
    customer_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_customer.id'), nullable=False)
    obu_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_obu.id'), nullable=False)
    sequence = db_pylang.Column(db_pylang.Integer, nullable=False)
    status = db_pylang.Column(db_pylang.Enum(Status), nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), nullable=False) # db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(), nullable=False)    # will be updated everytime there is update to this table

    obu = db_pylang.relationship(Obu, lazy='joined')

    def __init__(self, obu, sequence, status):
        self.obu = obu
        self.sequence = sequence
        self.status = status


class Wallet(db_pylang.Model):
    __tablename__ = "m_wallet"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    wallet_account_no = db_pylang.Column(db_pylang.String, nullable=False)
    initial_balance = db_pylang.Column(db_pylang.Numeric, nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), nullable=False)   #db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime  = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(), nullable=False)        #will be updated everytime there is update to this table

    def __init__(self, wallet_account_no, initial_balance):
        self.wallet_account_no = wallet_account_no
        self.initial_balance = initial_balance



class WalletCustomer(db_pylang.Model):
    __tablename__ = "m_wallet_customer"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    customer_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_customer.id'), nullable=False)
    wallet_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_wallet.id'), nullable=False)
    sequence = db_pylang.Column(db_pylang.Integer, nullable=False)
    issuer_code = db_pylang.Column(db_pylang.String, nullable=False)
    account_no_cid = db_pylang.Column(db_pylang.String, nullable=False)
    account_type = db_pylang.Column(db_pylang.String, nullable=False)
    status = db_pylang.Column(db_pylang.Enum(Status), nullable=False, default=Status.ACTIVE)
    default_sof_flag = db_pylang.Column(db_pylang.Enum(SOF), nullable=False, default=SOF.NOT_DEFAULT)
    balance = db_pylang.Column(db_pylang.Numeric, nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), nullable=False)  # db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(), nullable=False)   # will be updated everytime there is update to this table

    wallet = db_pylang.relationship(Wallet, lazy='joined')

    def __init__(self, wallet, sequence, issuer_code, account_no_cid, account_type, status, default_sof_flag, balance):
        self.wallet = wallet
        self.sequence = sequence
        self.issuer_code = issuer_code
        self.account_no_cid = account_no_cid
        self.account_type = account_type
        self.status = status
        self.default_sof_flag = default_sof_flag
        self.balance = balance



class Organization(db_pylang.Model):
    __tablename__ = "m_organization"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    name = db_pylang.Column(db_pylang.String)
    type = db_pylang.Column(Enum(OrganizationType), nullable=False)

    def __init__(self, name, type):
        self.name = name
        self.type = type



class OrganizationCommunication(db_pylang.Model):
    __tablename__ = "m_org_communication"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    organization_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_organization.id'), nullable=False)
    drc_ip_address = db_pylang.Column(db_pylang.String, nullable=False)
    prod_ip_address = db_pylang.Column(db_pylang.String, nullable=False)
    communication_method = db_pylang.Column(db_pylang.String, nullable=False)
    source_method = db_pylang.Column(db_pylang.String, nullable=False)
    cryptographic_type = db_pylang.Column(db_pylang.String, nullable=False)
    secret_key = db_pylang.Column(db_pylang.String, nullable=False)
    public_key = db_pylang.Column(db_pylang.String, nullable=False)
    ssl_certificate = db_pylang.Column(db_pylang.String, nullable=False)
    default_flag = db_pylang.Column(Enum(DefaultFlag), nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(),
                                 nullable=False)  # db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(),
                                 nullable=False)  # will be updated everytime there is update to this table

    organization = relationship("Organization", backref=backref("m_org_communication", uselist=False))

    def __init__(self, organization, drc_ip_address, prod_ip_address, communication_method, source_method, cryptographic_type, secret_key, public_key, ssl_certificate, default_flag ):
        self.organization = organization
        self.drc_ip_address = drc_ip_address,
        self.prod_ip_address = prod_ip_address
        self.communication_method = communication_method
        self.source_method = source_method
        self.cryptographic_type = cryptographic_type
        self.secret_key = secret_key
        self.public_key = public_key
        self.ssl_certificate = ssl_certificate
        self.default_flag = default_flag




class TransactionType(db_pylang.Model):
    __tablename__ = "m_transaction_type"

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    organization_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_organization.id'), nullable=False)
    fee_schema_id = db_pylang.Column(db_pylang.BIGINT, nullable=False)
    sequence = db_pylang.Column(db_pylang.Integer, nullable=False)
    trx_name = db_pylang.Column(db_pylang.String, nullable=False)
    recon_schedule_id = db_pylang.Column(db_pylang.BIGINT, nullable=False)
    settlement_id = db_pylang.Column(db_pylang.BIGINT, nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(),
                                 nullable=False)  # db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(),
                                 nullable=False)  # will be updated everytime there is update to this table

    organization = relationship("Organization", backref=backref("m_transaction_type", uselist=False))

    def __init__(self, organization, fee_schema_id, sequence, trx_name, recon_schedule_id, settlement_id):
        self.organization = organization
        self.fee_schema_id = fee_schema_id
        self.sequence = sequence
        self.trx_name = trx_name
        self.recon_schedule_id = recon_schedule_id
        self.settlement_id = settlement_id



class TransactionSummary(db_pylang.Model):
    __tablename__ = 'r_trans_summary_h'

    id = db_pylang.Column(db_pylang.BIGINT, primary_key=True, autoincrement=True)
    wallet_customer_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_wallet_customer.id'))
    transaction_type_id = db_pylang.Column(db_pylang.BIGINT, db_pylang.ForeignKey('m_transaction_type.id'))
    transaction_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), nullable=False)
    transaction_location = db_pylang.Column(db_pylang.String, nullable=False)
    transaction_amount = db_pylang.Column(db_pylang.Numeric, nullable=False)
    total_fee = db_pylang.Column(db_pylang.Numeric, nullable=False)
    total_amount = db_pylang.Column(db_pylang.Numeric, nullable=False)
    trans_recon_flag = db_pylang.Column(Enum(ReconFlag), nullable=False)
    trace_number = db_pylang.Column(db_pylang.String, nullable=False)
    created_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(),
                                 nullable=False)  # db_pylang.func.now => will be using the db_pylang.DateTime from server
    updated_datetime = db_pylang.Column(db_pylang.DateTime(timezone=True), server_default=db_pylang.func.now(), onupdate=db_pylang.func.now(),
                                 nullable=False)  # will be updated everytime there is update to this table

    transaction_type = relationship("TransactionType", backref=backref("r_trans_summary_h"))
    wallet_customer = relationship("WalletCustomer", backref=backref("r_trans_summary_h"))

    def __init__(self, transaction_type, transaction_datetime, transaction_location, transaction_amount, total_fee, total_amount, trans_recon_flag, trace_number, wallet_customer):
        self.transaction_type = transaction_type
        self.transaction_datetime = transaction_datetime
        self.transaction_location = transaction_location
        self.transaction_amount = transaction_amount
        self.total_fee = total_fee
        self.total_amount = total_amount
        self.trans_recon_flag = trans_recon_flag
        self.trace_number = trace_number
        self.wallet_customer = wallet_customer

