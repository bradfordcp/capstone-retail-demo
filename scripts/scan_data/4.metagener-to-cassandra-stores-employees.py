#!/usr/bin/env python

import calendar
import logging
import logging.handlers
import random
import requests
import time
import uuid

from decimal import Decimal
from flask import Flask
from six.moves import queue

from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory

# setup logger
logger = logging.getLogger('ingestion')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
logger.addHandler(ch)


def init_cassandra():
    """
    create Cassandra session
    :return: cluster, session
    """

    # grab ip address information from application.cfg
    app = Flask(__name__)
    app.config.from_pyfile('/cornerstone/flask/DataStaxDemo/application.cfg')
    ip_addresses = app.config['DSE_CLUSTER'].split(',')

    # connect to Cassandra
    cluster = Cluster(ip_addresses)
    session = cluster.connect()
    session.row_factory = ordered_dict_factory

    return cluster, session


def cleanup(futures, cluster, session):
    """
    Cleanup all pending threads before shutting down the Cluster() object
    :param futures: Queue of futures
    :param cluster: Cluster() object for shutdown()
    :param session: Session() object for retries
    :return:
    """
    while True:
        try:
            old_future = futures.get_nowait()
            old_future.result()
        except queue.Empty:
            break
        except Exception:
            logger.exception('Operation failed:')
            time.sleep(2)

            logger.info('Retrying: %s' % old_future.query)
            future = session.execute_async(old_future.query)
            futures.put_nowait(future)
    cluster.shutdown()


def async_write_full_pipeline(futures, session, prepared_statement, values):
    """
    Ensure the driver's pipeline stays full.
    :param futures: Queue of futures
    :param session: Cassandra session()
    :param prepared_statement: Prepared statement that will be executed
    :param values: Values to send with prepared statement
    :return:
    """

    # check if futures warmed up
    if futures.full():
        while True:
            # clear old future
            old_future = futures.get_nowait()
            try:
                old_future.result()
                break
            except Exception:
                logger.exception('Operation failed:')
                time.sleep(2)

                logger.info('Retrying: %s' % old_future.query)
                future = session.execute_async(old_future.query)
                futures.put_nowait(future)

    future = session.execute_async(prepared_statement, values)
    futures.put_nowait(future)


def populate_stores(futures, session):
    """
    Read from Metagener REST API and save data to Cassandra
    :param futures: queue.Queue
    :param session: Cassandra session()
    :return: None
    """

    rest_api = 'http://localhost:8080/bulksample/retail/retail.stores/'
    batch_size = 1
    endpoint = '%s%s' % (rest_api, batch_size)

    store_insert_statement = session.prepare(
        'INSERT INTO retail.stores (store_id, city, express_registers, full_registers, hours_close, '
        'hours_exceptions, hours_open, phones, state, street, tax_rate, zipcode) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
    zipcode_select_statement = session.prepare(
        'SELECT city, state FROM retail.zipcodes WHERE zipcode = ? LIMIT 1'
    )

    r = requests.get(endpoint).json()

    for store in r['sampleValues']:
        raw_values = store['fieldValues']

        # Read city and state from Zip code table
        rows = session.execute(zipcode_select_statement, [raw_values['zipcode']])

        values = {
            'store_id': int(raw_values['store_id']),
            'city': rows[0]['city'],
            'express_registers': int(raw_values['express_registers']),
            'full_registers': int(raw_values['full_registers']),
            'hours_close': None,
            'hours_exceptions': None,
            'hours_open': None,
            'phones': None,
            'state': rows[0]['state'],
            'street': "{} {}".format(raw_values['street_no'], raw_values['street']).encode('utf-8'),
            'tax_rate': Decimal(raw_values['tax_rate']),
            'zipcode': raw_values['zipcode']
        }

        async_write_full_pipeline(futures, session, store_insert_statement, values)


def populate_employees(futures, session):
    """
    Read from Metagener REST API and save data to Cassandra
    :param futures: queue.Queue
    :param session: Cassandra session()
    :return: None
    """

    rest_api = 'http://localhost:8080/bulksample/retail/retail.employees/'
    batch_size = 1
    endpoint = '%s%s' % (rest_api, batch_size)

    employee_insert_statement = session.prepare(
        'INSERT INTO retail.employees (employee_id, first_name, last_initial, last_name, store_id) '
        'VALUES (?, ?, ?, ?, ?)')

    r = requests.get(endpoint).json()

    for employee in r['sampleValues']:
        raw_values = employee['fieldValues']
        values = {
            'employee_id': int(raw_values['employee_id']),
            'first_name': raw_values['first_name'],
            'last_name': raw_values['last_name'],
            'last_initial': raw_values['last_initial'],
            'store_id': int(raw_values['store_id'])
        }
        async_write_full_pipeline(futures, session, employee_insert_statement, values)


def main():
    # set Cassandra futures queue size
    futures = queue.Queue(maxsize=31)

    # create Cassandra connections
    cluster, session = init_cassandra()

    populate_stores(futures, session)
    populate_employees(futures, session)

    # cleanup final requests
    cleanup(futures, cluster, session)


if __name__ == "__main__":
    main()
