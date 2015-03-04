#!/bin/sh

sudo sed -i -e "s|^SPARK_ENABLED=.*|SPARK_ENABLED=1|g" /etc/default/dse
