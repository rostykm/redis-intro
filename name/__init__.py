__author__ = 'rostyslavfedynyshyn'

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
r.set('foo2', 'bar')
print r.getrange('foo', 0, 10)

r.hmset('hashmap', {'key': 'value', 'int': '1'})
print r.hgetall('hashmap')

r.hincrby('hashmap', 'int', 1)
print r.hgetall('hashmap')

r.hset()

print r.hkeys('hashmap')
