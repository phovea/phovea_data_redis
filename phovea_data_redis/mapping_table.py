import logging

_log = logging.getLogger(__name__)


def create_db():
  import redis
  import phovea_server.config

  c = phovea_server.config.view('phovea_data_redis.mapping')

  # print c.hostname, c.port, c.db
  return redis.Redis(host=c.hostname, port=c.port, db=c.db)


class RedisMappingTable(object):
  def __init__(self, from_idtype, to_idtype):
    self.from_idtype = from_idtype
    self.to_idtype = to_idtype
    self._map = None

  def _load(self):
    from itertools import izip
    db = create_db()
    prefix = '{}2{}.'.format(self.from_idtype, self.to_idtype)
    keys = [k for k in db.scan_iter(match=prefix + '*')]
    values = db.mget(keys)

    self._map = dict()
    prefix_length = len(prefix)
    for key, value in izip(keys, values):
      from_id = key[prefix_length + 1:]
      self._map[from_id] = value.split(';')

  def __call__(self, ids):
    if not self._map:
      self._load()

    return [self._map.get(id, None) for id in ids]


def _discover_mappings():
  db = create_db()
  keys = [k for k in db.scan_iter(match='mappingFrom*')]
  for key in keys:
    key = key[len('mappingFrom') + 1:]
    parts = key.split('2')
    _log.info('loading redis mapping table from %s to %s', parts[0], parts[1])
    yield RedisMappingTable(parts[0], parts[1])


class RedisMappingProvider(object):
  def __init__(self):
    self._mappings = list(_discover_mappings())

  def __iter__(self):
    return iter(self._mappings)


def create():
  return RedisMappingProvider()
