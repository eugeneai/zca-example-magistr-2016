from nose.tools import raises
from zcaexample.components import People
from zcaexample.interfaces import IPeople, IDBConnection
from zope.component import getUtility
import redis


class TestBasicTest:
    def setUp(self):
        self.p = People

    def tearDown(self):
        pass

    def test_create_one_people(self):
        assert self.p is not None

    def test_implements(self):
        assert IPeople.implementedBy(self.p)


class TestRedis:
    def setUp(self):
        self.conn = redis.StrictRedis(
            host='localhost', port=6379, db=0)

    def tearDown(self):
        pass

    def test_set(self):
        assert self.conn.set('foo', 'bar')

    def test_get(self):
        self.test_set()
        foo = self.conn.get('foo')
        print(foo)
        assert foo == b'bar'

class TestAdapterForIPeopleToIStorableObject(object):
    def setUp(self):
        self.conn = getUtility(IDBConnection, name="main")
        self.p = People("Evgeny", "Cherkashin", "2513 880584")

    def test_save_load(self):
        _id = self.conn.save(self.p)
        assert _id is not None
        print("Saved as:", _id)
        o = self.conn.load(_id)
        print (o, self.p)
        assert o == self.p
