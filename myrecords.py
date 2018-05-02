from records import Database


class SimpleMysql(Database):
    @classmethod
    def _escape(cls, content):
        return str(content).replace('\\', '\\\\').replace('\'', '\\\'')

    def escape(self, content):
        return self._escape(content)

    def select(self, table=None, select_as="", condition=None, fields=None, left_join=None,
               order_by=None, order_direction="", limit=None, fetchall=True):
        """
        :param table: Table name you are going to query, string type: "a"
        :param select_as: Select table as name "select_as"
        :param condition: Where condition for the query, dict type: {"f1": "1", "f2":["in", ("1","2")], "f3": ["like", "abc%"]}
        :param fields: Table fields you are going to fetch, list type: ["name", "password"] or ['a.name', 'b.id']
        :param left_join: Left join tables, list type with dict items: [{"table":"blacklist", "asname":"b", "on": a.name == b.name}]
        :param order_by: Items used to order, string type
        :param order_direction: Order direction if needed, string type: "ASC", "DESC"
        :param limit: result Limitation, int or list or tuple type
        :param fetchall: If true, return a list of Record objects
        :return: If "fetchall" is False, return Record object; else return a list with Record objects

        Example:
                mydb = SimpleMysql('mysql://...')

                table = 'user'
                select_as = 'a'
                fields = ['a.user', 'b.id', 'c.permissions']
                left_join = [{'table': 'log', 'asname': 'b', 'on': 'a.user = b.user},
                    {'table': 'tickets', 'asname': 'c', 'on': 'a.id = c.uid'}]
                condition = {'a.user': 'test', 'b.groups': ['in', '("t1", "t2")'], 'c.location': ['like': 'Sh%']}

                result = mydb.select(table=table, select_as=select_as, fields=fields, left_join=left_join,
                    condition=condition, order_by="a.id", order_direction="DESC", limit=(10, 20))
        """
        _fields = self._fields_parse(fields, select_as)
        _select_as = "AS `%s` " % select_as
        _left_join = self._leftjoin_parse(left_join)
        _where = self._where_parse(condition, select_as)
        select_sql = "SELECT {fields} FROM `{table}` {select_as} {left_join} WHERE 1=1 {where}" \
            .format(fields=_fields, table=table, select_as=_select_as, left_join=_left_join, where=_where)
        if order_by:
            select_sql += " ORDER BY {0} {1}".format(order_by, order_direction)
        if limit:
            if isinstance(limit, (list, tuple)):
                select_sql += " LIMIT {0}, {1}".format(limit[0], limit[1])
            else:
                select_sql += " LIMIT {}".format(limit)
        return self.query(select_sql, fetchall=fetchall)

    def update(self, table, content, condition):
        update_sql = "UPDATE %s SET" % table
        for k, v in content.items():
            update_sql += " `%s` = '%s'," % (str(k), self.escape(v))
        update_sql = update_sql[:-1] + " WHERE 1=1"
        for k, v in condition.items():
            update_sql += " AND `%s` " % str(k)
            if isinstance(v, (list, tuple)):
                update_sql += " %s '%s'" % (v[0], self.escape(v[1]))
            else:
                update_sql += " = '%s'" % self.escape(v)
        if self.query(update_sql) is False:
            return False
        else:
            return True

    def insert(self, table, content, ignore=False):
        if ignore:
            insert_sql = "INSERT IGNORE INTO %s " % table
        else:
            insert_sql = "INSERT INTO %s " % table

        insert_sql += self._content_parse(content)
        return self.query(insert_sql)

    def replace(self, table, content):
        replace_sql = "REPLACE INTO %s" % table
        replace_sql += self._content_parse(content)
        return self.query(replace_sql)

    def delete(self, table, condition):
        delete_sql = "DELETE FROM %s WHERE 1=1" % table
        for k, v in condition.items():
            delete_sql += " AND `%s` " % str(k)
            if isinstance(v, (list, tuple)):
                delete_sql += " %s '%s'" % (v[0], self.escape(v[1]))
            else:
                delete_sql += " = '%s'" % self.escape(v)
        return self.query(delete_sql)

    def _content_parse(self, content):
        _k = ""
        _v = ""
        for k, v in content.items():
            _k += "`%s`," % str(k)
            _v += "'%s'," % self.escape(v)

        return "(%s) VALUES (%s)" % (_k[:-1], _v[:-1])

    @staticmethod
    def _leftjoin_parse(left_join):
        _left_join = ""
        if left_join:
            for join in left_join:
                if not isinstance(join, dict):
                    continue

                left_table = join.get('table')
                asname = join.get('asname')
                on = join.get('on')
                if not (left_table and on):
                    continue

                _left_join += "LEFT JOIN `{0}` AS `{1}` ON {2} ".format(left_table, asname, on)

        return _left_join

    def _where_parse(self, condition, select_as):
        _where = ""
        if condition:
            for k, v in condition.items():
                if select_as:
                    _where += " AND %s " % str(k)
                else:
                    _where += " AND `%s` " % str(k)
                if isinstance(v, (list, tuple)):
                    if v[0] == "in":
                        _where += " in %s" % (self.escape(v[1]))
                    else:
                        _where += " %s '%s'" % (v[0], self.escape(v[1]))
                else:
                    _where += " = '%s'" % self.escape(v)

        return _where

    @staticmethod
    def _fields_parse(fields, select_as):
        if fields:
            if not select_as:
                _fields = '`%s`' % "`,`".join(fields)
            else:
                _fields = ",".join(fields)
        else:
            _fields = "*"

        return _fields
