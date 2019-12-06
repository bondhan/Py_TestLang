
-- --------------------------------------------------------
-- use mysql;
-- SET GLOBAL max_connections = 1000;
-- commit;
-- show variables like 'max_connections';

start transaction;

-- --------------------------------------------------------

drop database pylang_db;
create database pylang_db;
-- --------------------------------------------------------

--
-- Table structure for table `m_customer`
--
use pylang_db;

CREATE TABLE `m_customer` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(14) NOT NULL,
  `email_address` varchar(45) NOT NULL,
  `first_name` varchar(35) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city_code` varchar(10) NOT NULL,
  `postal_code` char(5) NOT NULL,
  `country_code` char(2) NOT NULL,
  `identity_type` enum('KTP','SIM','PASPOR') NOT NULL,
  `identity_number` varchar(16) NOT NULL,
  `tax_code` varchar(15) NOT NULL,
  `created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_m_customer_phone_number (phone_number)
) ENGINE=InnoDB;


create table `m_obu` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `obu_id` varchar(32) NOT NULL,
	`serial_number_obu` varchar(50) NOT NULL,
	`aes_token_code` varchar(256) NOT NULL,
	`obu_manufacturer` varchar(20) NOT NULL,
    `initial_balance` NUMERIC(14,4) NOT NULL DEFAULT 0,
	`created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(id),
    index idx_m_obu_obu_id(obu_id),
	index idx_m_obu_serial_number_obu(serial_number_obu),
    unique key uk_m_obu_obu_id(obu_id),
	unique key uk_m_obu_serial_number_obu(serial_number_obu)
) engine=InnoDB;


CREATE TABLE `m_obu_customer` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `obu_id` BIGINT NOT NULL,
  `customer_id` BIGINT NOT NULL,
  `sequence` int NOT NULL,
  `status` enum('ACTIVE','INACTIVE') NOT NULL,
  `created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY fk_m_obu_customer_customer_id(customer_id) REFERENCES m_customer(id),
  FOREIGN KEY fk_m_obu_customer_obu_id(obu_id) REFERENCES m_obu(id),
  CONSTRAINT UC_m_obu_customer UNIQUE (customer_id,sequence)
) ENGINE=InnoDB;


CREATE TABLE `m_wallet` (
  `id` BIGINT NOT NULL auto_increment,
  `wallet_account_no` varchar(20) NOT NULL,
  `initial_balance` NUMERIC(14,4) NOT NULL DEFAULT 0,
  `created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  primary key(id)
) ENGINE=InnoDB;
--
create table `m_wallet_customer` (
    `id` BIGINT NOT NULL auto_increment,
    `wallet_id` BIGINT NOT NULL,
    `customer_id` BIGINT NOT NULL,
    `sequence` int NOT NULL,
    `issuer_code` varchar(4) NOT NULL,
    `account_no_cid` varchar(16) NOT NULL,
    `account_type` varchar(45) NOT NULL,
    `status` enum('ACTIVE','INACTIVE') NOT NULL default 'ACTIVE',
    `default_sof_flag` enum('DEFAULT','NOT_DEFAULT') NOT NULL default 'NOT_DEFAULT',
    `balance` numeric(14,4) NOT NULL DEFAULT 0,
    `created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(id),
    FOREIGN KEY fk_m_wallet_customer_customer_id(customer_id) REFERENCES m_customer(id),
    FOREIGN KEY fk_m_wallet_customer_wallet_id(wallet_id) REFERENCES m_wallet(id),
    CONSTRAINT UC_m_wallet_customer UNIQUE (customer_id,wallet_id, sequence)
) engine=InnoDb;


create table `m_organization` (
    `id` BIGINT NOT NULL auto_increment,
    `name` varchar(64) NOT NULL,
    `type` enum('BANK','OTHERS') NOT NULL,
    primary key(id)
) engine=InnoDb;

create table `m_org_communication`(
	`id` BIGINT NOT NULL auto_increment,
	`organization_id` BIGINT NOT NULL,
	`drc_ip_address` varchar(15) NOT NULL,
	`prod_ip_address` varchar(15) NOT NULL,
	`communication_method` varchar(20) NOT NULL,
	`source_method` varchar(20) NOT NULL,
	`cryptographic_type` varchar(10) NOT NULL,
	`secret_key` varchar(256) NOT NULL,
	`public_key` varchar(256) NOT NULL,
	`ssl_certificate` text NOT NULL,
	`default_flag` enum('DEFAULT','NOT_DEFAULT') not NULL,
	`created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(id),
	FOREIGN KEY fk_m_org_communication_organization_id(organization_id) REFERENCES m_organization(id)
) engine=InnoDb;


create table `m_transaction_type`(
	`id` BIGINT NOT NULL auto_increment,
	`fee_schema_id` BIGINT NOT NULL,
	`sequence` int NOT NULL,
	`trx_name` varchar(50) NOT NULL,
	`recon_schedule_id` BIGINT NOT NULL,
	`settlement_id` BIGINT NOT NULL,
	`organization_id` BIGINT NOT NULL,
	`created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key(id),
	FOREIGN KEY fk_m_transaction_type_organization_id(organization_id) REFERENCES m_organization(id)
)engine=InnoDb;

create table `r_trans_summary_h`(
	`id` BIGINT NOT NULL auto_increment,
	`wallet_customer_id` BIGINT NOT NULL,
	`transaction_type_id` BIGINT NOT NULL,
	`transaction_datetime` datetime NOT NULL,
	`transaction_location` varchar(45) NOT NULL,
	`transaction_amount` numeric(15,5) NOT NULL,
	`total_fee` numeric(15,5) NOT NULL,
	`total_amount` numeric(15,5) NOT NULL,
	`trans_recon_flag` enum('YES','NO') NOT NULL,
	`trace_number` varchar(64) NOT NULL,
	`created_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	primary key (id),
	FOREIGN KEY fk_r_trans_summary_h_wallet_customer_id(wallet_customer_id) REFERENCES m_wallet_customer(id),
	FOREIGN KEY fk_r_trans_summary_h_transaction_type_id(transaction_type_id) REFERENCES m_transaction_type(id)
)engine=innodb;

commit;
