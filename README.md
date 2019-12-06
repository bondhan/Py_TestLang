**Python Mockup for Texo E-Toll Payment**<br>
<br>
_**API CALL <-- REST/JSON --> API Server <-- REST/JSON --> ISO Client Server <-- ISO8583 --> ISO Server**_ <br>
<br>
**Requirements**<br>
- Python 3.7<br>
- Python 3.7 environment

**Setup Virtual Environment**<br>
bondhan@ubuntu:~$ python3.7 -m venv env<br>
bondhan@ubuntu:~$ ls<br>
env  workspace<br>
bondhan@ubuntu:~$ source env/bin/activate<br>
(env) bondhan@ubuntu:~$<br>
<br>
**Installing requirements**<br>
(env) bondhan@ubuntu:~$ pip3.7 install -r requirements.txt<br>
<br>
**Running**<br>
**API Server**<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang$ cd src/apiserver/<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/apiserver$ gunicorn -w 25 -b 0.0.0.0:5000 main_api_server:app_apiserver<br>
<br>
**ISO Client Server**<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/iso_client$ gunicorn -w 25 main_iso_client:app_isoclient -b 0.0.0.0:8080<br>
<br>
**ISO Server**<br>
<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang$ cd src/iso_server/<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/iso_server$ python3.7 main_iso_server.py<br>
<br>
**Database**<br>
- First run src/sql_db/01_schema_pylang.sql<br>
- populate the database by running python3.7 initialize_data_v2.py<br>

**Testing**<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang$ cd src/customer_input/<br>
(env) bondhan@ubuntu:~/workspace/python/Py_TestLang/src/customer_input$ python3.7 payment_test_v2.py<br>

#### Notes
The result could differ based on the machine configuration, how many thread, core processor, etc.. 
Initial test showing 1000 requests  took 6.974648475646973 seconds on **vmware** ubuntu linux server, 4 GB, 8 cores, 25 gunicorn workers with 50 threads testing threads
