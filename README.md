Caleydo Data Redis ![Caleydo Web Server Plugin](https://img.shields.io/badge/Caleydo%20Web-Server-10ACDF.svg)
=====================

Data provider plugin for loading data stored in a [Redis in-memory database](http://redis.io/).


Installation
------------

[Set up a virtual machine using Vagrant](http://www.caleydo.org/documentation/vagrant/) and run these commands inside the virtual machine:

```bash
./manage.sh clone Caleydo/caleydo_data_redis
./manage.sh resolve
```

If you want this plugin to be dynamically resolved as part of another application of plugin, you need to add it as a peer dependency to the _package.json_ of the application or plugin it should belong to:

```json
{
  "peerDependencies": {
    "caleydo_data_redis": "*"
  }
}
```

Usage
------------

The plugin is currently used to load ID mapping files.

### Load Mapping From File
To load mapping, put the mapping folder that includes the mapping txt files in the ```_data``` folder and run the following commands within the ```caleydo_data_redis``` plugin folder:
```python load_mappings.py```

### Flush Mapping Database

```bash
redis-cli

select 3
flushall
```

Administrating Redis from your host machine
------------

Follow this steps if you want to administrate the Redis instance that is installed inside the virtual machine (using Vagrant)

1. Download any Redis administration tool (e.g., [Redis Desktop Manager](https://redisdesktop.com/))
2. Create a new connection, save it, and connect
```
host: localhost
port: 6379
activate use ssh tunnel
SSH address: 127.0.0.1
SSH port: 2222
SSH user name: vagrant
SSH password: vagrant
```

***

<a href="https://caleydo.org"><img src="http://caleydo.org/assets/images/logos/caleydo.svg" align="left" width="200px" hspace="10" vspace="6"></a>
This repository is part of **[Caleydo Web](http://caleydo.org/)**, a platform for developing web-based visualization applications. For tutorials, API docs, and more information about the build and deployment process, see the [documentation page](http://caleydo.org/documentation/).
