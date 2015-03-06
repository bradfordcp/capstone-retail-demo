## Spark Streaming Analytics
Target would like a realtime dashboard displaying total sales by store on a trailing 1 hour basis. This system utilizes DataStax Enterprise with Spark Streaming to process a live field of store sales data.

We have been provided a supply script which sends live sales data to a socket. This data would traditionally pass through a queue. We have simulated a queueing system with netcat and a unix pipe. This copies the data from the data generator to the spark streaming interface.

Within the Spark job we set up a chain of filters to process the incoming data. Spark streaming handles converting the input data into batches. The first transform we perform removes any record starting with a '#'. This is used by the generator to indicate header values. We then split the line on the field delimiter, '::', which is then converted into a tuple of store_id and sale. These tuples are then reduced by the store_id key. Which builds a RDD of total sales by store. This RDD is then stored into Cassandra. Records are upserted which ensures the lastest data is always available.

It is worth noting that should a store not report data in a subsequent batch, their previous total sales value will persist.

Next we approached the frontend adding a graph to our dashboard. This exposes the collected analytics as a bar chart.

```cql
CREATE TABLE sale_counts (store_id INT PRIMARY KEY, total_sales DECIMAL);
```

