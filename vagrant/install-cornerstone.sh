#!/bin/sh

sudo pip install -r /capstone/flask/DataStaxDemo/requirements.txt

CACHE=/cache/gviz_api_py
if [ ! -d ${CACHE} ]; then
    wget -c https://google-visualization-python.googlecode.com/files/gviz_api_py-1.8.2.tar.gz -P /cache
    tar -zxvf /cache/gviz_api_py-1.8.2.tar.gz --directory /cache
    mv /cache/gviz_api_py*/ ${CACHE}
fi

(
    cd /cache/gviz_api_py
    sudo python setup.py install
)

(
    cd /capstone/flask/DataStaxDemo
    bower --config.analytics=false install
)

cqlsh 192.168.101.10 -f /capstone/cql/schema.cql

# seed stable data
/capstone/scripts/seed_retail_data/1.download-data.sh
/capstone/scripts/seed_retail_data/2.data-to-cassandra.py

# seed zipcode data
cp /capstone/scripts/seed_zipcode_data/free-zipcode-database.csv /cache
/capstone/scripts/seed_zipcode_data/1.zipcodes-to-cassandra.py

# start webserver for register scan data
/capstone/scripts/scan_data/1.extract-ids.py
/capstone/scripts/scan_data/2.extract-zipcodes.py
/capstone/scripts/scan_data/3.start-metagener.sh
## /capstone/scripts/scan_data/4.metagener-to-cassandra.py

CFG=/capstone/flask/DataStaxDemo/application.cfg
if [ ! -f ${CFG} ]; then
    # copy the template to its real location
    cp /capstone/flask/DataStaxDemo/application.cfg.template ${CFG}

    # generate new secret key and DSE IP addresses
    SECRET_KEY=$(openssl rand -base64 48)
    DSE_CLUSTER='192.168.101.10,192.168.101.11,192.168.101.12'

    # make replacements
    sed -i -e "s/^SECRET_KEY.*/SECRET_KEY = '${SECRET_KEY}'/" ${CFG}
    sed -i -e "s/^DSE_CLUSTER.*/DSE_CLUSTER = '${DSE_CLUSTER}'/" ${CFG}
fi
