import redis
import os

db = redis.Redis(host='localhost', port=6379, db=4)


def load_file(file_name):
  name, _ = os.path.splitext(os.path.basename(file_name))
  print 'loading '+file_name+' '+name
  with open(file_name, 'r') as f:
    for line in f:
      parts = [s.strip() for s in line.split('\t')]
      from_ = parts[0]
      key = name + '.' + from_
      if len(parts) != 2 or parts[1] == '-':
        db.delete(key)
        continue
      to = parts[1]
      db.set(key, to)

for p in os.listdir('../../_data/mappings/'):
  load_file(os.path.join('../../_data/mappings/', p))
