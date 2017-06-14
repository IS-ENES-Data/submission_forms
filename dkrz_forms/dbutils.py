
# sudo -i -u couchdb /home/couchdb/couchdb/bin/couchdb

import couchdb

couch = couchdb.Server('http://stephan:stephan123@localhost:5984')

# db = couch.create('test')


