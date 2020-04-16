\cp process_function.py __main__.py
zip -r -q couchdb_process_hail.zip __main__.py virtualenv 
wsk -i action update mypython/couchdb_process_hail couchdb_process_hail.zip --kind python:3
