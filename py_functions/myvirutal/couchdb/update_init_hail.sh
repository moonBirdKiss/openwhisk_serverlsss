\cp init_function.py __main__.py
zip -r -q couchdb_init_hail.zip __main__.py virtualenv 
wsk -i action update mypython/couchdb_init_hail couchdb_init_hail.zip --kind python:3
