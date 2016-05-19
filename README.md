## Caleydo Data Redis Plugin ![Caleydo Web Server Plugin](https://img.shields.io/badge/Caleydo%20Web-Server-9E25BD.svg)

Data provider plugin for loading data stored in a [Redis in-memory database](http://redis.io/) for [Caleydo Web](https://caleydo.org).

### How to Install

Within the Caleydo Web Development Environment run:
```
./manage.sh install caleydo_tooltip
```

### How to Use

The plugin is currently used to load ID mapping files.

#### Load Mapping From File
To load mapping, put the mapping folder that includes the mapping txt files in the ```_data``` folder and run the following commands within the ```caleydo_data_redis``` plugin folder:
```python load_mappings.py```

#### Flush Mapping Database

```bash
redis-cli

select 3
flushall
```

*****

<a href="https://caleydo.org"><img src="http://caleydo.org/assets/images/logos/caleydo.svg" align="left" width="200px" hspace="10" vspace="6"></a>
This plugin is part of **[Caleydo Web](http://caleydo.org/)**, a platform for developing web-based visualization applications. For tutorials, API docs, and more information about the build and deployment process, see the [documentation page](http://caleydo.org/documentation).
