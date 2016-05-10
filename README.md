Caleydo Data Redis
==================

[Redis](http://redislabs.com/) based id manager. In the long run a key-value store adapter

flush mapping db:
```bash
redis-cli

select 3
flushall
```

To load mapping, put the mapping folder that includes the mapping txt files in the ```_data``` folder and run the following commands within the caleydo_data_redis plugin folder:
```python load_mappings.py```
