
def ascii(s):
  return s

import logging
_log = logging.getLogger(__name__)

class RedisIDAssigner(object):
  """
  assigns ids to object using a redis database
  """
  def __init__(self):
    import redis
    import caleydo_server.config

    c = caleydo_server.config.view('caleydo_data_redis.assigner')

    #print c.hostname, c.port, c.db
    self._db = redis.Redis(host=c.hostname, port=c.port, db=c.db)

  @staticmethod
  def to_forward_key(idtype, identifier):
    return ascii(idtype + '2id.' + str(identifier))

  @staticmethod
  def to_backward_key(idtype, id):
    return ascii('id2' + idtype + '.' + str(id))

  def unmap(self, uids, idtype):
    idtype = ascii(idtype)
    def lookup(id):
      key = self.to_backward_key(idtype, id)
      return self._db.get(key)
    return map(lookup, uids)

  def __call__(self, ids, idtype):
    """
     return the integer index ids for the given ids in the given idtype
    """
    idtype = ascii(idtype)

    before = self._db.get(idtype) if self._db.exists(idtype) else self._db.decr(idtype) #initialize with -1
    def lookup(id):
      key = self.to_forward_key(idtype, id)
      i = self._db.get(key)
      if i is not None:
        return int(i)
      i = self._db.incr(idtype)
      self._db.set(key,i)
      self._db.set(self.to_backward_key(idtype, i),str(id))
      return i
    r = map(lookup, ids)

    after = int(self._db.get(idtype))
    if before != after:
      _log.debug('create %s %d!=%d',idtype,before,after)

    return r

def create():
  _log.info('create redis assigner')
  return RedisIDAssigner()
