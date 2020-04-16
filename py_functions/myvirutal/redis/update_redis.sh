\cp redis_hail.py __main__.py
zip -r -q redis_hail.zip __main__.py virtualenv 
wsk -i action update mypython/redis_hail redis_hail.zip --kind python:3
