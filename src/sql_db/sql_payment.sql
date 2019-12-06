use pylang_db;

select cst.id, wallet.id, cst.first_name, (cst.last_name + cst.phone_number) as username from m_customer as cst
    inner join m_obu_customer as obu_cst on cst.id = obu_cst.customer_id inner join m_obu as obu on obu_cst.obu_id = obu.id inner join m_wallet_customer as wallet_cst on wallet_cst.customer_id = cst.id
    inner join m_wallet as wallet on wallet.id = wallet_cst.wallet_id where obu.serial_number_obu='11AA22BB33CC4400' and wallet_cst.default_sof_flag = 'DEFAULT';


select cst.id, wallet.id, cst.first_name, (cst.last_name + cst.phone_number) as username, obu.serial_number_obu, wallet_cst.balance
	from m_customer as cst
    inner join m_obu_customer as obu_cst on cst.id = obu_cst.customer_id
    inner join m_obu as obu on obu_cst.obu_id = obu.id
    inner join m_wallet_customer as wallet_cst on wallet_cst.customer_id = cst.id
    inner join m_wallet as wallet on wallet.id = wallet_cst.wallet_id
    where wallet_cst.default_sof_flag = 'DEFAULT';


