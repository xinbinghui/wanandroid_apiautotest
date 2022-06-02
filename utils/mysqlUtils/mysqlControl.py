import MySQLdb
from common.setting import ConfigHandler
from utils.readfilesUtils.yamlControl import GetYamlData
from utils.otherUtils.get_conf_data import sql_switch
from utils.readfilesUtils.regularControl import sql_regular
from utils.logUtils.logControl import ERROR

class MysqlDB:
    if sql_switch():

        def __init__(self):
            self.config = GetYamlData(ConfigHandler.config_path)
            self.read_mysql_config = self.config.get_yaml_data()['MySqlDB']

            try:
                # 建立数据库连接
                self.conn = MySQLdb.connect(
                    host=self.read_mysql_config['host'],
                    user=self.read_mysql_config['user'],
                    password=self.read_mysql_config['password'],
                    db=self.read_mysql_config['db']
                )
                # 使用 cursor 方法获取操作游标，得到一个可以执行sql语句，并且操作结果为字典返回的游标
                self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            except Exception as e:
                ERROR.logger.error("数据库连接失败, 失败原因{0}".format(e))
        
        def __del__(self):
            try:
                # 关闭游标
                self.cur.close()
                # 关闭连接
                self.conn.close()
            except Exception as e:
                ERROR.logger.error("数据库连接失败, 失败原因{0}".format(e))
        
        def query(self, sql, state='all'):
            """
            查询
            :param sql:
            :param state: all 是默认查询全部
            :return:
            """
            try:
                self.cur.execute(sql)

                if state == 'all':
                    data = self.cur.fetchall()
                
                else:
                    # 查询单条
                    data = self.cur.fetchone()
                
                return data
            except Exception as e:
                ERROR.logger.error("数据库连接失败, 失败原因{0}".format(e))

        def execute(self, sql):
            """
            更新、删除、新增
            :param sql:
            :return:
            """
            try:
                # 使用excute操作sql
                rows = self.cur.execute(sql)
                # 提交事务
                self.conn.commit()
                return rows
            except Exception as e:
                ERROR.logger.error("数据库连接失败, 失败原因{0}".format(e))
                # 如果事务异常，则回滚数据
                self.conn.rollback()

        def assert_execution(self, sql, rep):
            """
            执行sql, 负责处理yaml文件中的断言需要执行多条sql的场景, 最终会将所有数据以对象形式返回
            :param sql: sql
            :param rep: 接口响应数据
            :return:
            """
            try:
                if isinstance(sql, list):
                    data = {}
                    if 'UPDATE' and 'update' and 'DELETE' and 'delete' and 'INSERT' and 'insert' in sql:
                        raise ValueError("断言的sql必须是查询的sql")
                    else:
                        for i in sql:
                            # 判断sql中是否有正则，如果有则通过jsonpath提取相关的数据
                            sql = sql_regular(i, rep)
                            # for 循环逐条处理断言 sql
                            query_data = self.query(sql)[0]
                            # 将sql返回的所有内容全部放入对象中
                            for key, value in query_data.items():
                                data[key] = value

                        return data
                else:
                    raise ValueError("断言的查询sql需要是list类型")
            except Exception as e:
                ERROR.logger.error("数据库连接失败, 失败原因{0}".format(e))

        def setup_sql_data(self, sql):
            """
            处理前置请求sql
            :param sql:
            :return:
            """
            data = {}
            if isinstance(sql, list):
                for i in sql:
                    sql_data = self.query(i)[0]
                    for key, value in sql_data.items():
                        data[key] = value
                return data