from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy

# 创建会话
def create_key_space(keyspacename,ster):
    session = ster.connect()
    return session

# 连接会话(获取指定keyspace的会话连接)
def connect_key_space():
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    # 数据库名
    keyspacename = "test"
    session = ster.connect(keyspace=keyspacename)
    return session

# 打印会话连接key_spaces
def print_key_spaces(ster):
    print("-------打印会话连接key_spaces------")
    print(ster.metadata.keyspaces)
    print("-----------------------------------")

# 打印表单tables
def print_tables(ster,keyspacename):
    print("------------打印表单tables---------")
    print(ster.metadata.keyspaces[keyspacename].tables)
    print("-----------------------------------")

def exist_table(table_name,keyspacename):
    '''判断表是否存在'''
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    session = ster.connect()
    print(ster.metadata.keyspaces[keyspacename].tables.keys())
    session.shutdown()
    if table_name in ster.metadata.keyspaces[keyspacename].tables.keys():
        return True
    return False

def exist_keyspace(keyspace):
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    session = ster.connect()
    print(ster.metadata.keyspaces.keys())
    session.shutdown()
    if keyspace in ster.metadata.keyspaces.keys():
        return True
    return False

def keyandspace():
    ster = Cluster(contact_points=['127.0.0.1'],
                   port=9042,
                   load_balancing_policy=RoundRobinPolicy())
    session = ster.connect()
    if not exist_keyspace("test"):
        session.execute("CREATE KEYSPACE test WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")

    if not exist_table("picrecog","test"):
        session.execute('create table test.picrecog(inserttime varchar,predictres int,filepath varchar primary key);')
    session.shutdown()

def insert_data(filepath,crtime,predictres):
    '''插入数据'''
    keyandspace()
    session = connect_key_space()
    sql = 'insert into picrecog(filepath,inserttime,predictres) values(%s, %s, %s)'
    session.execute(sql, (filepath, crtime, predictres))
    session.shutdown()

def showdata():
    # 查询所有
    keyandspace()
    session = connect_key_space()
    sql = 'select * from picrecog'
    rs = session.execute(sql)
    session.shutdown()
    return rs

rr = showdata()
print(rr.current_rows)