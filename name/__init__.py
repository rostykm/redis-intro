__author__ = 'rostyslavfedynyshyn'

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

print '---keys---'
r.set('foo', 'bar')
r.set('foo2', 'bar')
print r.getrange('foo', 0, 10)

print '---hashmap---'
r.hmset('hashmap', {'key': 'value', 'int': '1'})
print r.hgetall('hashmap')

r.hincrby('hashmap', 'int', 1)
r.hset('hashmap', 'int', '6')
print r.hgetall('hashmap')
print r.hkeys('hashmap')
# ?\print 'lenght' + r.hlen('hasmap')

print '---hyperloglog---'

from datetime import datetime
start = datetime.now()
for i in xrange(10):
    r.pfadd('hyperloglog', i)

end = datetime.now()
print end - start

start = datetime.now()
print r.pfcount('hyperloglog')
end = datetime.now()
print end - start

start = datetime.now()
for i in xrange(100):
    r.lpush('list', i)
end = datetime.now()
print end - start

start = datetime.now()
print r.llen('list')
end = datetime.now()
print end - start

r.flushall()
