# Parsing ```brands.txt``` and ingesting into Cassandra
This portion of the project had us ingesting the supplied brands.txt.gz text file into the brands tables. We began by inspecting the schema of the table and contents of the ```brands.txt``` file. We determined that each brand entry began with a 10 character id (of uppercase letters and numbers), followed by a space, with the rest of the line constituting the brand name.

Since we already had working code for the products table we use this as a basis when starting the brand parsing and insertion logic. We modified the matching regex to fit the brand format we identified previously. Logic for fields not present in the brands table was removed. Next we updated the ```INSERT``` CQL statement to point at the right table and columns.

At this point we tested our ingestion script, taking note of any issues. The first item centered on issues with UTF-8 encoding and invalid character sequences. We extracted the brands.txt.gz file and interrogated it's encoding with ```file -bi brands.txt.gz```. From here we determined that the appropriate encoding was ```ISO-8859-1```. We modified our ingestion logic to decode the line into ```UTF-8```.

Next there were some issues with blank values being ingested. We added logic to check the length of a brand. If the length is 0 the record is skipped. We also went back looked at the lines which were surfacing blank values and verified that they were indeed empty.

Finally we took on the task of data parity. Marc put together an awesome unix command to get a total count of valid, unique brand names. He then performed a count of all of the lines to compare with the count in Cassandra. We then compared this number to a COUNT query run in both ```cqlsh``` and ```spark```.

```cql
SELECT COUNT(*) FROM retail.brands LIMIT 5000;
```

```scala
hc.sql("SELECT * FROM retail.brands").count()
```

```unix

```
