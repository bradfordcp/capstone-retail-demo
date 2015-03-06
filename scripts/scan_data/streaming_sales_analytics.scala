
// Within the last hour, what has been the store's total sales

val product_line = """8235::16::1dca3e00-c39e-11e4-8080-808080808080::1425604460::0::1::B00009UT1Q::Sunpak MINI-PLUS Mini Tripod with 3-Way Panhead::11.0740::12.9500::1.8760"""
val product = product_line.split("::")
BigDecimal.double2bigDecimal("2.8".toDouble)


// CREATE TABLE sale_counts (store_id INT PRIMARY KEY, total_sales DECIMAL);

import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
import com.datastax.spark.connector.streaming._
import com.datastax.spark.connector.cql.CassandraConnector

// Setup Spark Conf and Streaming Context
val conf = new SparkConf().setMaster("local[3]").setAppName("NetworkSalesCount")
val ssc = new StreamingContext(conf, Seconds(60))

// Look for data at our simulated queue on port 5006
val lines = ssc.socketTextStream("localhost", 5006)

// Remove products that being with a # and split on '::'
val products = lines.filter(! _.startsWith("#")).map(product_line => product_line.split("::"))

// Generate a tuple with the store_id and item price
val analytic_items = products.map(product => (product(0).toString, BigDecimal.double2bigDecimal(product(8).toDouble)))

// Reduce the datset to generate a total by store
val analytic_counts = analytic_items.reduceByKey(_ + _)

// Save results to table and display
analytic_counts.saveToCassandra("retail", "sale_counts", SomeColumns("store_id", "total_sales"))
analytic_counts.print()

// Start the streaming context
ssc.start()
