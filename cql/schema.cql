CREATE KEYSPACE retail WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'Cassandra': '3'
};

USE retail;

CREATE TABLE brands (
  name TEXT,
  PRIMARY KEY ((name))
);

CREATE TABLE products (
  id TIMEUUID,
  title TEXT,
  price DOUBLE,
  brand TEXT,
  PRIMARY KEY ((id))
);

CREATE TABLE stores (
  region_id TIMEUUID,
  district_id TIMEUUID,
  id TIMEUUID,
  address TEXT,
  phone_numbers MAP<TEXT,TEXT>,
  hours MAP<TEXT,TEXT>,
  num_express_registers INT,
  num_full_registers INT,
  tax_rate MAP<TEXT,FLOAT>,
  PRIMARY KEY((id))
);

CREATE TABLE employees (
  id TIMEUUID,
  name TEXT,
  last_initial TEXT,
  store_id TIMEUUID,
  PRIMARY KEY ((id))
);

CREATE TABLE registers (
  id TIMEUUID,
  region_id TIMEUUID,
  district_id TIMEUUID,
  store_id TIMEUUID,
  receipt_id TIMEUUID,
  product_id TIMEUUID,
  price MAP<TEXT, DOUBLE>,
  scan_time TIMESTAMP,
  PRIMARY KEY ((id))
);

CREATE TABLE receipts (
  id TIMEUUID,
  region_id TIMEUUID,
  district_id TIMEUUID,
  store_id TIMEUUID,
  cashier TIMEUUID,
  drawer_closing_time TIMESTAMP,
  total DOUBLE,
  payment MAP<TEXT,DOUBLE>,
  PRIMARY KEY ((id))
);

CREATE TABLE receipts_registers (
  receipt_id TIMEUUID,
  register_id TIMEUUID,
  region_id TIMEUUID STATIC,
  district_id TIMEUUID STATIC,
  store_id TIMEUUID STATIC,
  cashier TIMEUUID STATIC,
  drawer_closing_time TIMESTAMP STATIC,
  total DOUBLE STATIC,
  payment MAP<TEXT, DOUBLE>,
  product_id TIMEUUID,
  price MAP<TEXT, DOUBLE>
  scan_time TIMESTAMP,
  PRIMARY KEY ((receipt_id), register_id)
);


