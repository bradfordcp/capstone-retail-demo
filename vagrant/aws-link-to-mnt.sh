#!/bin/sh

sudo mkdir -p /mnt/lib/cassandra
sudo mkdir -p /mnt/log/cassandra

sudo chown cassandra:cassandra /mnt/lib/cassandra
sudo chown cassandra:cassandra /mnt/log/cassandra

sudo rm -rf /var/lib/cassandra
sudo rm -rf /var/log/cassandra

sudo ln -s /mnt/lib/cassandra /var/lib
sudo ln -s /mnt/log/cassandra /var/log

sudo chown -R cassandra:cassandra /var/lib/cassandra
sudo chown -R cassandra:cassandra /var/log/cassandra
