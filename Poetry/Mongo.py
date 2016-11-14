# coding=utf-8

"""
1. 封装数据库操作(INSERT,FIND,UPDATE)
2. 函数执行完MONGODB操作后关闭数据库连接
"""
from pymongo.database import Database

try:
    from pymongo import MongoClient
except ImportError:
    # 好像2.4之前的pymongo都没有MongoClient,现在官网已经把Connection抛弃了
    import warnings
    warnings.warn("Strongly recommend upgrading to the latest version pymongo version,"
                  "Connection is DEPRECATED: Please use mongo_client instead.")
    from pymongo import Connection as MongoClient

class Mongo(object):

    '''封装数据库操作'''
    def __init__(self, host='localhost', port=27017, database='poetry',
                 maxPoolSize=10, timeout=10):
        self.host = host
        self.port = port
        self.maxPoolSize = maxPoolSize
        self.timeout = timeout
        self.database = database

    @property
    def connect(self):
        # 我这里是为了使用类似"db.集合.操作"的操作的时候才会生成数据库连接,其实pymongo已经实现了进程池,也可以把这个db放在__init__里面,
        # 比如我把db关掉有其他的数据库调用连接又会生成,并且不影响使用.我这里只是想每次执行数据库生成一个连接用完关掉-自己控制自己的
        return MongoClient(self.host, self.port, maxPoolSize=self.maxPoolSize,
                  connectTimeoutMS=1000 * self.timeout)

    def __getitem__(self, collection):
        # 为了兼容db[集合].操作的用法
        return self.__getattr__(collection)

    def __getattr__(self, collection_or_func):
        db = self.connect[self.database]
        if collection_or_func in Database.__dict__:
            # 当调用的是db的方法就直接返回
            return getattr(db, collection_or_func)
        # 否则委派给Collection
        return Collection(db, collection_or_func)

class Collection(object):

    def __init__(self, db, collection):
        self.collection = getattr(db, collection)

    def __getattr__(self, operation):
        # 我这个封装只是为了拦截一部分操作,不符合的就直接raise属性错误
        control_type = ['disconnect', 'insert', 'insert_one', 'update', 'find', 'find_one']
        if operation in control_type:
            return getattr(self.collection, operation)
        raise AttributeError(operation)


def close_db(dbs=['db']):
    '''
    关闭mongodb数据库连接
    db : 在执行函数里面使用的db的名字(大部分是db，也会有s_db)
        Usage::
            >>>s_db = Mongo()
            >>>@close_db(['s_db'])
            ...: def test():
            ...:     print s_db.test.insert({'a': 1, 'b': 2})
            ...:
    '''
    def _deco(func):
        @wraps(func)
        def _call(*args, **kwargs):
            result = func(*args, **kwargs)
            for db in dbs:
                try:
                    func.func_globals[db].connection.disconnect()
                except KeyError:
                    pass
            return result
        return _call
    return _deco