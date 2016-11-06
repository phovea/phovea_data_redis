import phovea_server.plugin


def ascii(s):
  return s


class MappingTable(object):
  def __init__(self, plugin):
    self.mappings = plugin.mappings
    self._plugin = plugin
    self._instance = None

  def __call__(self, from_idtype, to_idtype, ids):
    if self._instance is None:
      self._instance = self._plugin.load().factory()
    return self._instance(from_idtype, to_idtype, ids)


class MappingManager(object):
  """
  assigns ids to object using a redis database
  """

  def __init__(self):
    mappers = [MappingTable(c) for c in phovea_server.plugin.list('mapping_table')]
    self.mappers = {}
    for m in mappers:
      for mapping in m.mappings:
        self.mappers[mapping] = m

  def can_map(self, from_idtype, to_idtype):
    from_idtype = ascii(from_idtype)
    to_idtype = ascii(to_idtype)

    key = from_idtype + '2' + to_idtype
    return key in self.mappers

  def maps_to(self, from_idtype):
    from_idtype = ascii(from_idtype)

    return [t for s, t in (s.split('2') for s in self.mappers.iterkeys()) if s == from_idtype]

  def __call__(self, from_idtype, to_idtype, ids):
    from_idtype = ascii(from_idtype)
    to_idtype = ascii(to_idtype)

    key = from_idtype + '2' + to_idtype
    if key in self.mappers:
      return self.mappers[key](from_idtype, to_idtype, ids)
    # no known mapping
    return [None for _ in ids]


def create():
  return MappingManager()
