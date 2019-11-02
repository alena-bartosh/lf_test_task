# Queries Calculation API

This is a home test task in which I worked with data in pandas dataframe, implemented Flask microservice (service API that follows REST standard) with Docker containerization and wrote unittests.
  
### Quick start with Docker
```
$ git clone https://github.com/alena-bartosh/lf_test_task.git && cd lf_test_task/
$ ./start.sh
```
Open http://0.0.0.0:5000/ to find examples of endpoints usage :satellite:

### Setup developer environment
```
$ git clone https://github.com/alena-bartosh/lf_test_task.git && cd lf_test_task/
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

### Run unittests
(in the virtual environment)
```
$ python3 -m unittest discover tests
```

### Run service
(in the virtual environment)
```
$ python3 main.py
```

### Time of execution of requests
(service should be ran)
```
$ ./requests_time.sh
```
On my laptop (Intel® Core™ i5-7200U CPU @ 2.50GHz × 4) I have the following results (only total time) for maximum coverage of test data:
```
/elapsed_time
0,003847s

/rows_per_second
0,006226s

/rows_per_thread
0,039862s

/thread_per_second
0,555200s
```
