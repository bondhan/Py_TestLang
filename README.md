# Python Mockup for Payment Simulation

### Introduction
A complete simulation of payment system using python flask. I simulate end2end call from client to the host (financial institutions) which mostly communicate using ISO8583. Below is the information flow:

**API CALL <-- (Rest/Json) --> API Server <-- (Rest/Json) --> ISO Client Server <-- (ISO8583) --> ISO Server**

### Requirements

- Python 3.7<br>
- Python 3.7 environment

#### Setup Virtual Environment
```bondhan@ubuntu:~$ python3.7 -m venv env
bondhan@ubuntu:~$ ls
env  workspace
bondhan@ubuntu:~$ source env/bin/activate
(env) bondhan@ubuntu:~$
```

#### Installing requirements
```
(env) bondhan@ubuntu:~$ pip3.7 install -r requirements.txt
```

#### Running
**API Server**
```
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang$ cd src/apiserver/
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/apiserver$ gunicorn -w 25 -b 0.0.0.0:5000 main_api_server:app_apiserver
```

**ISO Client Server**
```
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/iso_client$ gunicorn -w 25 main_iso_client:app_isoclient -b 0.0.0.0:8080
```

**ISO Server**
```
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang$ cd src/iso_server/
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/iso_server$ python3.7 main_iso_server.py
```

**Database**
- First run src/sql_db/01_schema_pylang.sql
- populate the database by running python3.7 initialize_data_v2.py

**Testing**
```
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang$ cd src/customer_input/
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/customer_input$ python3.7 payment_test_v2.py
```

#### Notes
The result could differ based on the machine configuration, how many thread, core processor, etc.. 
Initial test showing 1000 requests  took 6.974648475646973 seconds on **vmware** ubuntu linux server, 4 GB, 8 cores, 25 gunicorn workers with 50 threads testing threads
