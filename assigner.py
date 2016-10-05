import logging

_log = logging.getLogger(__name__)
from itertools import izip


def ascii(s):
  return s


class RedisIDAssigner(object):
  """
  assigns ids to object using a redis database
  """

  def __init__(self):
    import redis
    import caleydo_server.config

    c = caleydo_server.config.view('caleydo_data_redis.assigner')

    # print c.hostname, c.port, c.db
    self._db = redis.Redis(host=c.hostname, port=c.port, db=c.db)

    from werkzeug.contrib.cache import SimpleCache
    self._cache = SimpleCache(threshold=16384)

  @staticmethod
  def to_forward_key(idtype, identifier):
    return ascii(idtype + '2id.' + str(identifier))

  @staticmethod
  def to_backward_key(idtype, id):
    return ascii('id2' + idtype + '.' + str(id))

  def _get_entry(self, key):
    r = self._cache.get(key)
    if r is not None:  # cached
      return r
    r = self._db.get(key)  # lookup in db
    if r is not None:  # cache if found
      self._cache.set(key, r)
    return r

  def _get_entries(self, keys):
    result = {}
    not_cached = []
    for k in keys:
      cached = self._cache.get(k)
      if cached is not None:  # cached
        result[k] = self._cache.get(k)
      else:
        not_cached.append(k)

    values = self._db.mget(not_cached)
    for k, v in izip(not_cached, values):
      if v:
        self._cache.set(k, v)
        result[k] = v
    return result

  def unmap(self, uids, idtype):
    idtype = ascii(idtype)
    entries = self._get_entries((self.to_backward_key(idtype, id) for id in uids))
    return [entries.get(self.to_backward_key(idtype, id), None) for id in uids]

  def load(self, idtype, mapping):
    """
    resets and loads the given mapping
    :param idtype:
    :param mapping: array of tuples (id, uid)
    :return:
    """
    idtype = ascii(idtype)

    # assuming incremental ids
    if idtype in self._db:
      _log.info('clearing %s', idtype)
      self._cache.clear()
      forward_keys = self._db.keys(idtype + '2id.*')
      _log.debug('found %d forward keys', len(forward_keys))
      self._db.delete(forward_keys)
      backward_keys = self._db.keys('id2' + idtype + '.*')
      _log.debug('found %d backwards keys', len(backward_keys))
      self._db.delete(backward_keys)
      _log.debug('deleted %d keys', len(backward_keys) + len(forward_keys))
      del self._db[idtype]

    if len(mapping) == 0:
      return  # no mappings to load

    max_uid = None
    pipe = self._db.pipeline()

    _log.info('%s loading %s keys', idtype, len(mapping))
    for id, uid in mapping:
      key = self.to_forward_key(idtype, id)
      max_uid = uid if max_uid is None else max(uid, max_uid)
      pipe.set(key, uid)
      pipe.set(self.to_backward_key(idtype, uid), str(id))

    pipe.set(idtype, max_uid)
    _log.debug('flushing')

    pipe.execute()
    _log.debug('flushed')

  def __call__(self, ids, idtype):
    """
     return the integer index ids for the given ids in the given idtype
    """
    idtype = ascii(idtype)

    before = int(self._db.get(idtype) if idtype in self._db else self._db.decr(idtype))  # initialize with -1
    entries = self._get_entries((self.to_forward_key(idtype, id) for id in ids))

    def lookup(id):
      key = self.to_forward_key(idtype, id)
      i = entries.get(key, None)
      if i is not None:
        return int(i)
      i = self._db.incr(idtype)
      self._db.set(key, i)
      self._cache.set(key, i)
      back_key = self.to_backward_key(idtype, i)
      self._db.set(back_key, str(id))
      self._cache.set(back_key, str(id))
      return i

    r = map(lookup, ids)

    after = int(self._db.get(idtype))
    if before != after:
      _log.debug('create %s %d!=%d', idtype, before, after)

    return r


def create():
  _log.info('create redis assigner')
  return RedisIDAssigner()
