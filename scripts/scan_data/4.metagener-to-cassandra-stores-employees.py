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

    pass


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
