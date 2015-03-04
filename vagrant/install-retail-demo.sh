#!/bin/sh

#cqlsh 192.168.101.10 -f /cornerstone/cql/schema.cql
cqlsh 127.0.0.1 -f /cornerstone/cql/schema.cql

# seed stable data
/cornerstone/scripts/seed_retail_data/1.download-data.sh
/cornerstone/scripts/seed_retail_data/2.data-to-cassandra.py

# seed zipcode data
cp /cornerstone/scripts/seed_zipcode_data/free-zipcode-database.csv /cache
/cornerstone/scripts/seed_zipcode_data/1.zipcodes-to-cassandra.py

# start webserver for register scan data
/cornerstone/scripts/scan_data/1.extract-ids.py
/cornerstone/scripts/scan_data/2.extract-zipcodes.py
/cornerstone/scripts/scan_data/3.start-metagener.sh
## /cornerstone/scripts/scan_data/4.metagener-to-cassandra.py
