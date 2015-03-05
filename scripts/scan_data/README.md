## Start metagener as a web service

The third script prepares and starts the metagener tools as a web service.
It filters out the entity ids which are needed to use generated data
with pre-generated data. It then starts the web service with a config
descriptor that preloads the data generator recipes from retail.metagener.
Data samples are then available at

- http://localhost:8080/sample/retail/register_scan

