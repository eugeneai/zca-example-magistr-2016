from zcaexample.interfaces import IPeople, IStorableObject, IDBConnection
from zope.interface import implementer
from zope.component import getGlobalSiteManager, adapter
import redis

class Animal(object):
    pass

@implementer(IPeople)
class People(Animal):
    def __init__(self, name, family, passport):
        self.name=name
        self.family=family
        self.passport=passport

    def fio(self):
        print("{} {}".format(self.name, self.family))

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        if self.name != other.name:
            return False
        if self.family != other.family:
            return False
        if self.passport != other.passport:
            return False
        return True

"""
@implementer(IGroup)
class Group(....):
    def __init__(self, name):
        self.name = name

class AdapterIGroupToIStorableObject(object):
    __init__(... obj)


    def save_into(self, conn):

    def load_from(self, conn):

"""

@implementer(IStorableObject)
@adapter(IPeople)
class AdapterForIPeopleToIStorableObject(object):
    def __init__(self, obj=None, id=None):
        if obj is not None:
            assert IPeople.providedBy(obj)
        elif id is None:
            raise ValueError("Neither obj nor id is supplied")
        self.obj = obj
        self._id = id

    def save_into(self, conn, id):
        obj = self.obj
        d={}
        d["name"] = obj.name
        d["family"] = obj.family
        d["passport"] = obj.passport
        txt = repr(d)
        print("Save as", id)
        conn.conn.set(id, txt.encode('utf-8'))
        self._id = id

    def load_from(self, conn):
        assert self.obj is None
        assert self._id is not None
        print(self._id)
        txt = conn.conn.get(self._id)
        assert txt is not None
        d = eval(txt.decode("utf-8"))
        self.obj = People(
            name = d["name"],
            family = d["family"],
            passport = d["passport"],
        )


@implementer(IDBConnection)
class RedisConnection(object):
    def __init__(self, host='localhost', port=6379, db=0):
        self.conn = redis.StrictRedis(host=host, port=port, db=db)
        self._id = 0
        self.load_id()

    def load_id(self):
        _id = self.conn.get("__id__",)
        if _id is not None:
            self._id=int(_id)
        else:
            self._id=0

    def save_id(self):
        self.conn.set("__id__", str(self._id).encode('utf-8'))

    def next_id(self, obj):
        self._id+=1
        self.save_id()
        return "{}-{}".format(obj.__class__.__name__,self._id)

    def save(self, obj):
        # assert IStorableObject.providedBy(obj)
        obj = IStorableObject(obj)
        _id = self.next_id(obj)
        class_name, key = _id.split("-")
        obj.save_into(self, key)
        return _id

    def load(self, id):
        """
        People-234234234
        """
        class_name, key = id.split("-")
        cls=globals()[class_name]
        obj=cls(id=key)
        obj.load_from(self)
        return obj.obj



GSM=getGlobalSiteManager()

connection=RedisConnection(host='localhost', port=6379, db=0)

GSM.registerUtility(connection, name="main")
GSM.registerAdapter(AdapterForIPeopleToIStorableObject)
