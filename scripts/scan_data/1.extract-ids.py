#!/usr/bin/env python

from flask import Flask
from cassandra.cluster import Cluster
from cassandra.query import dict_factory


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
    session.row_factory = dict_factory

    return cluster, session


def cleanup(cluster):
    """
    Cleanup all pending threads before shutting down the Cluster() object
    :param futures: Queue of futures
    :param cluster: Cluster() object for shutdown()
    :param session: Session() object for retries
    :return:
    """

    cluster.shutdown()


# Writes all product ids to /cache/product_ids.txt
def retrieve_product_ids(session, path):
    rows = session.execute("SELECT product_id FROM retail.products")

    f = open(path, 'w')

    i = 0
    update_rate = 10000
    for row in rows:
        i += 1
        f.write("{}\n".format(row['product_id']))

        if i % update_rate == 0:
            print("Processed {} rows".format(i))

    print("Finished {} rows".format(i))
    f.close()


def main():
    # create Cassandra connections
    cluster, session = init_cassandra()

    # Retrieve product ids
    retrieve_product_ids(session, '/cache/product_ids.txt')

    # cleanup final requests
    cleanup(cluster)


if __name__ == "__main__":
    main()
