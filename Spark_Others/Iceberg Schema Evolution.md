# Apache Spark Iceberg Operations
### This document shows Iceberg Schema Evolution operations with Apache Spark in Ezmeral Unified Analytics  
#### Entire workflow is run as an Apache Spark Application with S3 as Storage. The Storage is provided by Ezmeral Data Fabric.
#### The connectivity to S3 can be either direct or via S3 Proxy in Ezmeral Unified Analytics
##### Iceberg Apache Spark Documentation: https://iceberg.apache.org/docs/nightly/spark-getting-started/

###### 1. Create or Replace test table 
```sql
create or replace table local.default.kafka_ingest3 as select * from local.default.kafka_ingest5 limit 300
select * from local.default.kafka_ingest3 limit 10
```
###### Output:
```

+-----+--------------------+--------------------+------+
|   id|                name|             address|amount|
+-----+--------------------+--------------------+------+
|64137|         Dustin Rich|9956 Nicholas Pra...|873737|
|72614|          Seth Cooke|4087 Kenneth Vall...| 56174|
|33598|       Linda Gilbert|USS Garcia\nFPO A...|486316|
|75619|       Gregory Payne|635 Jones River S...|431140|
|13122|    Jacqueline Allen|5990 Blair Park S...|684473|
|99059|   Tamara Montgomery|002 Zachary Well ...| 92321|
|58934|Christopher Thompson|6090 Matthew Fore...|862928|
| 6339|        Derek Kelley|8120 Kyle Tunnel ...|368548|
|26778|          Edgar Kidd|7515 Long Springs...|272445|
|18444|       Andrea Henson|19150 Mark Knolls...|777686|
+-----+--------------------+--------------------+------+

```


###### 2. Add a new column and then rename the column
```sql
alter table local.default.kafka_ingest3 add column selcol varchar(10)
alter table local.default.kafka_ingest3 rename column selcol to highval
```
###### Output:
```

+-----+--------------------+--------------------+------+------+
|   id|                name|             address|amount|selcol|
+-----+--------------------+--------------------+------+------+
|64137|         Dustin Rich|9956 Nicholas Pra...|873737|  NULL|
|72614|          Seth Cooke|4087 Kenneth Vall...| 56174|  NULL|
|33598|       Linda Gilbert|USS Garcia\nFPO A...|486316|  NULL|
|75619|       Gregory Payne|635 Jones River S...|431140|  NULL|
|13122|    Jacqueline Allen|5990 Blair Park S...|684473|  NULL|
|99059|   Tamara Montgomery|002 Zachary Well ...| 92321|  NULL|
|58934|Christopher Thompson|6090 Matthew Fore...|862928|  NULL|
| 6339|        Derek Kelley|8120 Kyle Tunnel ...|368548|  NULL|
|26778|          Edgar Kidd|7515 Long Springs...|272445|  NULL|
|18444|       Andrea Henson|19150 Mark Knolls...|777686|  NULL|
+-----+--------------------+--------------------+------+------+

+-----+--------------------+--------------------+------+-------+
|   id|                name|             address|amount|highval|
+-----+--------------------+--------------------+------+-------+
|64137|         Dustin Rich|9956 Nicholas Pra...|873737|   NULL|
|72614|          Seth Cooke|4087 Kenneth Vall...| 56174|   NULL|
|33598|       Linda Gilbert|USS Garcia\nFPO A...|486316|   NULL|
|75619|       Gregory Payne|635 Jones River S...|431140|   NULL|
|13122|    Jacqueline Allen|5990 Blair Park S...|684473|   NULL|
|99059|   Tamara Montgomery|002 Zachary Well ...| 92321|   NULL|
|58934|Christopher Thompson|6090 Matthew Fore...|862928|   NULL|
| 6339|        Derek Kelley|8120 Kyle Tunnel ...|368548|   NULL|
|26778|          Edgar Kidd|7515 Long Springs...|272445|   NULL|
|18444|       Andrea Henson|19150 Mark Knolls...|777686|   NULL|
+-----+--------------------+--------------------+------+-------+

```


###### 3. Update added column to identify 400k or more in amount
```sql
update local.default.kafka_ingest3 set highval = 'y' where amount > 400000
```
###### Output:
```

+-----+--------------------+--------------------+------+-------+
|   id|                name|             address|amount|highval|
+-----+--------------------+--------------------+------+-------+
|64137|         Dustin Rich|9956 Nicholas Pra...|873737|      Y|
|72614|          Seth Cooke|4087 Kenneth Vall...| 56174|   NULL|
|33598|       Linda Gilbert|USS Garcia\nFPO A...|486316|      Y|
|75619|       Gregory Payne|635 Jones River S...|431140|      Y|
|13122|    Jacqueline Allen|5990 Blair Park S...|684473|      Y|
|99059|   Tamara Montgomery|002 Zachary Well ...| 92321|   NULL|
|58934|Christopher Thompson|6090 Matthew Fore...|862928|      Y|
| 6339|        Derek Kelley|8120 Kyle Tunnel ...|368548|   NULL|
|26778|          Edgar Kidd|7515 Long Springs...|272445|   NULL|
|18444|       Andrea Henson|19150 Mark Knolls...|777686|      Y|
+-----+--------------------+--------------------+------+-------+

```


###### 4. Use added column to list out 400k or more in amount clients
```sql
select * from local.default.kafka_ingest3 where highval = 'y'
```
###### Output:
```

+-----+--------------------+--------------------+------+-------+
|   id|                name|             address|amount|highval|
+-----+--------------------+--------------------+------+-------+
|64137|         Dustin Rich|9956 Nicholas Pra...|873737|      Y|
|33598|       Linda Gilbert|USS Garcia\nFPO A...|486316|      Y|
|75619|       Gregory Payne|635 Jones River S...|431140|      Y|
|13122|    Jacqueline Allen|5990 Blair Park S...|684473|      Y|
|58934|Christopher Thompson|6090 Matthew Fore...|862928|      Y|
|18444|       Andrea Henson|19150 Mark Knolls...|777686|      Y|
|22881|        Laura Taylor|197 Jorge Pine Ap...|427515|      Y|
|18636|   Christopher White|7042 Lucas Freewa...|588851|      Y|
|83946|        Jacob Phelps|062 Hayes Cove Su...|726606|      Y|
|55536|     Tiffany Stewart|76866 Catherine S...|706646|      Y|
| 6694|        Michelle May|275 Hector Port\n...|762485|      Y|
|95513|      Andres Pearson|191 Diana Orchard...|826370|      Y|
|49022|         Aaron Russo|613 Cowan Extensi...|812542|      Y|
|27030|      Robert Carroll|25894 Shannon Pik...|696476|      Y|
| 2920|       Crystal Petty|7866 Ramirez Isla...|459429|      Y|
|  424|           Alan Gill|8774 Karla River ...|651362|      Y|
|90379|      Samuel Mcguire|3530 Gaines Roads...|929239|      Y|
|77528|        Shawn Nguyen|USNV Smith\nFPO A...|459279|      Y|
|  840|   Christopher James|2102 Angelica Vie...|922995|      Y|
|10484|       Craig Aguilar|9162 Brandi Lake ...|466008|      Y|
+-----+--------------------+--------------------+------+-------+
only showing top 20 rows-+

