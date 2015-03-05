## Loading data from REST API into Cassandra
Started by firing up the Metagener jar. We then pulled a URL from the python script to analyze the output from metagener for employees. With this information available we started mapped the available fields to the appropriate CQL types and column names. Metagener only provides Strings, which we then coerced into ints, utf-8 string, and Decimal.  We used a prepared statement as the batch size will be increased in the future. The prepared statement will provide excellent performance.

For the stores table we did not have city and state information available. We had to consume the zipcode value from metagener, then perform a read against the zipcodes table for the city and state. With this information available we combined the metagener output, with type coercion, and the query results to form the values to insert. Again we used prepared statements for the insert and select as they will both be reused.

