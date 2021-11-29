import psycopg2
from psycopg2 import pool
from .logger import Logger


class PostgresQL(object):
    def __init__(self):
        self.logger = Logger().logtoFile()
        self.postgresql_min = 10
        self.postgresql_max = 50
        self.user = "admin"
        self.password = "admin@123"
        self.host = "172.27.230.22"
        self.port = "5432"
        self.db = "postgres"

        self.connect = None
        self.pool = None

    def get_pool(self):
        if self.pool is not None:
            self.logger.info("Connect to DB: %s:%s/%s" % (self.host, self.port, self.db))
            return self.pool

        return self._create_pool()

    def _create_pool(self):
        try:
            self.pool = pool.ThreadedConnectionPool(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db,
                minconn=self.postgresql_min,
                maxconn=self.postgresql_max
            )

        except Exception as e:
            self.logger.error("%s" % (e), exc_info=True)
        else:
            self.logger.debug("Connect to DB: %s:%s/%s" % (self.host, self.port, self.db))
            return self.pool

    def get_connection(self):
        if self.connect is not None:
            return self.connect

        return self._create_connect()

    def _create_connect(self):
        try:
            self.connect = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db
            )

        except Exception as err:
            self.logger.error("%s" %err, exc_info=True)
        else:
            return self.connect

    def select_query(self, sql, data=None):
        results = None
        connect = None
        cursor = None
        cur_result = None
        try:
            connect = self.get_connection()
            if connect is not None:
                self.logger.debug("Get Cursor")

                cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
                self.logger.debug("%s" % (cursor))

            if cursor is not None:
                self.logger.debug("Init SQL with data: %s" % data)

                if data is not None:
                    cursor.execute(sql, data)
                else:
                    cursor.execute(sql, )
                cur_result = cursor.fetchall()

                self.logger.debug("Result SQL %s" % len(
                    cur_result) if cur_result is not None else 0)
        except Exception as e:
            self.logger.error("%s" % (e), exc_info=True)
            return False
        except psycopg2.DatabaseError.pgerror as e:
            self.logger.error("%s" % (e), exc_info=True)
            return False
        else:
            if cur_result is not None:
                results = [dict(row) for row in cur_result]
                return results

            return results
        finally:
            if cursor is not None:
                cursor.close()
                connect.close()

    def excute_query(self, sql, data=None):
        results = None
        connect = None
        cursor = None
        cur_result = None
        try:
            connect = self.get_connection()
            if connect is not None:
                cursor = connect.cursor()

            if cursor is not None:
                if data is None:
                    cursor.execute(sql)

                elif isinstance(data, list):
                    cursor.executemany(sql, data)
                else:
                    cursor.execute(sql, data)
                cur_result = cursor.rowcount
                connect.commit()
        except psycopg2.DatabaseError.pgerror as e:
            self.logger.error("%s" % (e), exc_info=True)
            return False
        except Exception as e:
            self.logger.error("%s" % (e), exc_info=True)
            return False
        else:
            if cur_result is not None:
                results = cur_result
                return results
            return results
        finally:
            if cursor is not None:
                cursor.close()
                connect.close()


postgresql_db = PostgresQL()
