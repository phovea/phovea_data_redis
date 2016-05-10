Caleydo Data Redis
==================

Data provider plugin for loading data stored in a [Redis in-memory database](http://redis.io/).

This plugin is part of the [Caleydo Web platform](http://caleydo.org/documentation).

![Caleydo Logo](http://caleydo.org/assets/images/logos/caleydo.svg)

Usage Information
-----------------

The plugin is currently used to load ID mapping files.

flush mapping db:
```bash
redis-cli

select 3
flushall
```

To load mapping, put the mapping folder that includes the mapping txt files in the ```_data``` folder and run the following commands within the caleydo_data_redis plugin folder:
```python load_mappings.py```
