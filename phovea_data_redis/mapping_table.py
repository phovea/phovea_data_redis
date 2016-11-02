
def ascii(s):
  return s

class RedisMappingTable(object):
  """
  assigns ids to object using a redis database
  """
  def __init__(self):
    import redis
    import phovea_server.config

    c = phovea_server.config.view('phovea_data_redis.mapping')

    #print c.hostname, c.port, c.db
    self._db = redis.Redis(host=c.hostname, port=c.port, db=c.db)

  def __call__(self, from_idtype, to_idtype, ids):
    from_idtype = ascii(from_idtype)
    to_idtype = ascii(to_idtype)

    key = from_idtype+'2'+to_idtype

    def lookup(id):
      fkey = key+'.'+ascii(id)
      r = self._db.get(fkey)
      if r is None:
        return None
      return r.split(';')

    return map(lookup, ids)

def create():
  return RedisMappingTable()

