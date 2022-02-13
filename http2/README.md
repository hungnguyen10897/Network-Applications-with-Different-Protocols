
Run server:

```
python server.py
```

Send request:

```
hyper --h2 GET http://localhost:8080/ gps:'60.1694098 24.9373494'
```

or

```
python client.py
```
and modify your trace header or uncomment 1 of the following trace

```
# Invalid GPS
# trace = [[121212, 24.927370699999997]]

# Invalid GPS
# trace = route[80:98] + [[121212, 24.927370699999997]]

# Espoo -> Helsinki -> Espoo
# trace2 = route[80:98]
# trace2.reverse()
# trace = route[80:98] + trace2

# Helsinki -> Espoo
trace = route[80:98]
trace.reverse()

# Espoo -> Helsinki
# trace = route[80:98]
```