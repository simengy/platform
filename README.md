# platform
ETL modules to access mysql database

There are three parts to start:

1. connection: using pyodbc to access mysql database

2. metric: collecting the features for model building

3. constraint: training model and optimizing for threshold

Phase 1 is finished. Milestone:

Current system could be running automatically to calculate metrics and find the constraints for time-series data/metrics.

Phase 2:

Generic Connectors -- MySQL, PIG/HIVE, Spark?
Generic data formats -- scalar, key-value pair, tree
library installation -- R/Python data format re-wrapper for smoother programming
More models -- descision tree, gradient boosting, ANOVA and more

