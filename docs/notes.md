## Dumping the product_ids to a file
We need to generate a product_ids file for Metagener. For this process we copied over the boilerplate logic for setting up and shutting down the connection to Cassandra. Next we created a method which queries the products table for ```product_id``` values. The rows were then iterated over and dumped to a file. In this case we did not use a prepared statement. There were no query parameters and it was executed a single time.

We added some output lines to indicate progress. When the script completes we are outputing the total number of lines processed.
