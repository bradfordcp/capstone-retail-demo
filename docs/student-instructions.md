# Student Instructions

For your final project, the following page contains all the necessary instructions.
Ensure you obtain a good grasp of what this schedule will be
requiring from you. We understand this is asking for a full three day commitment,
so please treat this time exactly as you would if you were on-site
with a high-profile company executing a high-valued deal.



> DataStax is working on a $50 million deal with Target. They plan on
rolling out fully connected retail B&M stores to get ready for this year's
Black Friday. Because of their high throughput and business use cases,
Target requires a highly available system to track every purchase across
all of their registers in each of their 30,000 stores by region, internationally.
DataStax is their answer but due to high demand of DataStax Enterprise experts,
Target looking to outsource their DataStax Enterprise consultants to
other DataStax Certified Partners. This is where you come in.




# Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Grading Process](#grading-process)
  - [Documentation](#documentation)
    - [Strategic In-Line Comments](#strategic-in-line-comments)
    - [Summary Documentation Comments](#summary-documentation-comments)
  - [Project Differences](#project-differences)
    - [Interactive Projects](#interactive-projects)
    - [Individual Projects](#individual-projects)
  - [Schedule](#schedule)
  - [Open Source Contributions](#open-source-contributions)
    - [Repository Layout](#repository-layout)
- [Day 1](#day-1)
  - [Data Modeling](#data-modeling)
    - [Interactive Project: Create a Schema Using Customer Specifications](#interactive-project-create-a-schema-using-customer-specifications)
    - [Individual Project: Create a More Elaborate Schema and Proposal for Future Business](#individual-project-create-a-more-elaborate-schema-and-proposal-for-future-business)
- [Day 2](#day-2)
  - [Cornerstone](#cornerstone)
    - [Interactive Project: Get the Cornerstone Running](#interactive-project-get-the-cornerstone-running)
  - [Data Migration](#data-migration)
    - [Interactive Project: Read From a Static File into Cassandra](#interactive-project-read-from-a-static-file-into-cassandra)
    - [Individual Project: Read From Metagener (REST API) into Cassandra](#individual-project-read-from-metagener-rest-api-into-cassandra)
  - [Front End](#front-end)
    - [Interactive Project: Display Charts Using the Cornerstone Infrastructure](#interactive-project-display-charts-using-the-cornerstone-infrastructure)
    - [Individual Project: Implement a New Google Chart](#individual-project-implement-a-new-google-chart)
  - [Spark SQL](#spark-sql)
    - [Instructions](#instructions)
    - [Interactive Project: Find the Most Efficient Employee per Store](#interactive-project-find-the-most-efficient-employee-per-store)
    - [Individual Project: Choose Your Own Adventure](#individual-project-choose-your-own-adventure)
- [Day 3](#day-3)
  - [Presentation](#presentation)
    - [Team Project: Present the Capstone](#team-project-present-the-capstone)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->




# Grading Process

## Documentation

Articulating with the customer is essential to ensuring a successful interaction.
Documentation is a key form of communication and it should be expected that you
are able to deliver a detailed account of what you've accomplished. Not only
is documentation crucial for the customer, it will be our basis for grading you.

For specific point allocation, 100% of the points of graded projects will be
pulled from our grading rubric for technical choices and implementations.

In order to be graded, you will need to document what you have done by using
Strategic In-Line Comments and Summary Documentation Comments which are described
below.


### Strategic In-Line Comments

Strategic comment example:

    By setting keys (X, Y) as the partition key and A, B as the clustering keys
    we ensure that our writes are ordered on disk in fashion M. However,
    when processing read requests having a compound partition key requires the
    user to provide both (X, Y) which is a guaranteed input given that N.

Functional comment example:

    X and Y are the partition keys and A and B are the clustering keys that will
    be sorted on disk. Reads will be efficient due to this on-disk ordering.

### Summary Documentation Comments

Summary documentation example:

    Given the schema that has been implemented, all writes will be require
    keys (X), Y, Z which guarantee batch updates, although typically never
    recommended, will execute efficiently since updates will all go to a single
    machine for processing and ensure the updates are still atomic when using
    UNLOGGED BATCH statements. Going with UNLOGGED BATCH, while ensuring the
    partition key is the same, ensures both atomicity and performant writes
    for this specific use case that requires A.

## Project Differences

### Interactive Projects

Interactive projects will occur in a mix of class-wide collaboration and team
execution. It is expected that DataStax Certified Partners be able to lead
brainstorming sessions during in-house POC implementations. Leadership
will be valued positively, however, so will ability to be collaborative.

Different implementations and workflows are guaranteed to occur and are
encouraged. Grading will occur based on ability to reason through a given
problem, successfully articulate reasoning, defend positioning, and equally
important: ability to collaboratively implement the solution(s).

### Individual Projects

Individual projects will take the lessons learned from interactive projects and
apply them during team-only execution. Discussions on broader implementations
are not expected, but highly encouraged.

## Schedule

Much like the final certification test, this entire schedule is expected to be
overly ambitious, but perhaps attainable in certain situations. Speeding past
the schedule will not inherently be penalized, but lack of collaboration during
interactive projects will cause all the groups to suffer.

Leading the way by a relatively large gap in the schedule also isn't valued as
highly as ensuring teams closest to your location on the schedule are able
to execute as effectively. Being a DataStax Certified Partner means having the
ability to not only execute, but to lead in a way that resonates with customers
long after the DataStax Certified Partner has departed.

## Open Source Contributions

All projects and code must inherit the Apache License and be executed with the
highest standards available due to planned open source distribution of all
content.

However, for the duration of the training all team repos will be private repos.
Once training is complete, access to the private repos will be granted to all
members of the training event for personal review and comparison. After the
repos have undergone grading, the best forks will submit a pull request to
the master project repo and automatically be open-sourced, referenced, and
used to showcase the power of DataStax Enterprise.

### Repository Layout

Pull requests must not contain modifications to the master infrastructure repo
since those pull requests must happen on the master infrastructure repo directly.

    datastax-demos
        |--- [public/infrastructure] cornerstone
                |---- [public/project] capstone-retail-demo
                        |---- [private/team] capstone-retail-demo-team-awesome
                        |---- [private/team] capstone-retail-demo-big-data-nerds
                        |---- [private/team] capstone-retail-demo-big-dataowski
                        |---- ...
                |---- [public/project] capstone-financial-fire-sale
                        |---- [private/team] capstone-retail-demo-team-awesome
                        |---- [private/team] capstone-retail-demo-big-data-nerds
                        |---- [private/team] capstone-retail-demo-big-dataowski
                        |---- ...
                |---- ...



# Day 1


## Data Modeling

### Interactive Project: Create a Schema Using Customer Specifications

> Provide Target with a customized data model to ensure their use cases are
wildly successful by creating an efficient well thought out schema along an
articulate proposal.

[Ideal Schema](../cql/schema.cql)

Create a schema that adheres the given constructs. Some data points are
intentionally left vague and in such cases considering the use case is a
requirement.

* A single keyspace named `retail` that will have 3 replicas.
* A table, `brands`, containing all known brand names.
* A table, `products`, containing:
    * prices
    * titles
    * product ids
    * brands
* A table, `stores`, containing:
    * number of express registers
    * number of full registers
    * store ids
    * store addresses
    * store phone numbers
    * store hours
    * tax rates
* A table, `employees`, containing:
    * last initial (to protect against accidental privacy leaks)
    * names
    * store ids
    * employee ids
* A table, `registers`, containing:
    * register ids
    * quantity of items
    * item information
    * price information
        * sales price
        * msrp
        * savings
    * scan times
    * store ids
    * receipt ids
* A table, `receipts`, containing:
    * receipt ids
    * store ids
    * register ids
    * cashier information
    * drawer closing time
    * total information
    * payment information

### Individual Project: Create a More Elaborate Schema and Proposal for Future Business

> Target has the perfect use case for an additional set of services that you
can provide with infrastructure that already exists or is trivial to purchase
and implement for a full roll out across all stores. Work at creating a full
schema and proposal to ensure that their DataStax Enterprise cluster is
properly used to the best of it's ability.

Elaborate further off the [official schema](../cql/schema.cql) to create a more
complex schema using event driven data collection as well as analytical tables.
These tables should come with full descriptions of how data will be collected,
results would be useful, analytics would be run, and any other information
that would be needed for a successful proposal.


# Day 2

From this point forward you will be working in pairs. Please pair off.

## Cornerstone

### Interactive Project: Get the Cornerstone Running

> Proof of Concepts are standard requests and requirements at some locations.
In order to help facilitate the DataStax Partner Network in building these demos,
DataStax has provided the Cornerstone project to ease the development of new
demos and POCs.

We'll cover a bit of the infrastructure and how to get the
Cornerstone project running, as well as how to contribute back into the DataStax
Demo Portal.



## Data Migration

### Interactive Project: Read From a Static File into Cassandra

> Target has a bit of stale data they'll use to seed their receipt rows. Help
them import CSV files into Cassandra using the DataStax Drivers.

Read from a CSV file into Cassandra.

### Individual Project: Read From Metagener (REST API) into Cassandra

> Target not only needs a POC for performance verification, but also something
tangible for their business model. Ensure you can generate the right type
and amount of data to convince them how powerful Cassandra is.

Using Jonathan Shook's [Metagener](https://github.com/jshook/metagener) read
data from a REST API and efficiently write the data into DataStax Enterprise.




## Front End

### Interactive Project: Display Charts Using the Cornerstone Infrastructure

> Target requires a basic listing of all products in their inventory. Make
sure your POC is able to effectively and efficiently display the requested
information.

Use the table view and a chart view. An in-class presentation will cover
the [REST API documenation](../rest-api.md) that touches on both the paging API
as well as the integrated charts API.

### Individual Project: Implement a New Google Chart

> Target requires a different view of the data to match a familiar style at the
project manager level.

Add two new charts and submit a pull request to the Cornerstone project.



## Spark SQL

### Instructions

1. Spark worker memory: set to 8192 in spark-env.sh
2. Increase max heap to 7500 MB in cassandra-env.sh
3. Restart DSE
4. Start the 4.xxx.sh as soon as possible, leave it running for 15 minutes, at
minimum, prior to the start of the exercise.
5. Bring up port 4040 and port 7080 on your browser, this will be monitoring
metrics for Spark execution, for the remainder of your Spark related exercise.
6. Checkout HiveContext (hc) and CassandraSQLContext (csc), and try each Context
individually.

### Interactive Project: Find the Most Efficient Employee per Store

> Target wants to start rewarding their fastest scanning employees through a
company-wide incentive program. Create a Spark job for them to be run monthly
to find their most efficient Employees of the Month.

Follow an in-class presentation for how to setup, write, and execute Spark jobs.
Write the resulting top performers into a Cassandra table for simple consumption
through the charting infrastructure.

### Individual Project: Choose Your Own Adventure

> Target is still on the fence of whether to go with DataStax Enterprise or
OSS Apache Cassandra. Help cement the business value of DataStax Enterprise with
a query, or set of queries, that can transform their data to the next level.

Follow the previous example's foundation to build a unique set of queries that
will be placed into their own Cassandra table for simple consumption through
the charting infrastructure.

# Day 3

## Presentation

### Team Project: Present the Capstone

> Target expects their consultants to deliver top-notch documentation and
a presentation that summarizes the approaches taken. This presentation should
reflect the main selling points of DataStax Enterprise for Target's use case.
In addition, it is crucial to leverage cutting-edge offerings, like Spark, that
can provide Target real-time analytics with the native performance wins of the
DataStax Enterprise suite.

For this presentation, assume you are presenting what you achieved to Target
as a DataStax Certified Partner. Think about what is most important for them to
hear from you. Plan for the following:

* A 30 minute presentation
* Q&A of 10 minutes
* Every person in your group should present
