phovea_data_redis [![Phovea][phovea-image]][phovea-url] [![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Dependency Status][daviddm-image]][daviddm-url]
=====================

Data provider plugin for loading data stored in a [Redis in-memory database](http://redis.io/).

Installation
------------

```
git clone https://github.com/phovea/phovea_data_redis.git
cd phovea_data_redis
npm install
```

Testing
-------

```
npm run test
```

Building
--------

```
npm run build
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
This repository is part of **[Phovea](http://phovea.caleydo.org/)**, a platform for developing web-based visualization applications. For tutorials, API docs, and more information about the build and deployment process, see the [documentation page](http://caleydo.org/documentation/).


[phovea-image]: https://img.shields.io/badge/Phovea-Server%20Plugin-10ACDF.svg
[phovea-url]: https://phovea.caleydo.org
[npm-image]: https://badge.fury.io/js/phovea_data_redis.svg
[npm-url]: https://npmjs.org/package/phovea_data_redis
[travis-image]: https://travis-ci.org/phovea/phovea_data_redis.svg?branch=master
[travis-url]: https://travis-ci.org/phovea/phovea_data_redis
[daviddm-image]: https://david-dm.org/phovea/phovea_data_redis.svg?theme=shields.io
[daviddm-url]: https://david-dm.org/phovea/phovea_data_redis
