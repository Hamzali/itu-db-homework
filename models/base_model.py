from utils import db_factory_func


class BaseModel:
	"""
	Base class for the data manipulation and database operations.
	"""

	def __init__(self, table, fields, init_table=False):
		self.table_name = table
		self.fields = fields
		if init_table:
			self.__init_table()

	@db_factory_func()
	def __init_table(conn, self):
		"""
		Initializes the database.
		"""
		try:
			# TODO: do not send a query use a clever way.
			conn.execute("SELECT * FROM {} ".format(self.table_name))
		except Exception as e:
			print(e)
			table_fields = []
			for field in self.fields:
				table_fields.append(field + " " + self.fields[field])
			init_query = "CREATE TABLE {} ( {} )".format(self.table_name, str.join(",", table_fields))

			try:
				conn.execute(init_query)
			except Exception as e:
				print(e)

	@db_factory_func()
	def create(conn, self, data):
		values = []
		for field in data:
			if self.fields.get(field) is not None:
				values.append("%({})s".format(field))

		if len(values) > 0:
			sql_statement = """INSERT INTO {}
							({}) 
							VALUES 
							({}) 
							""".format(self.table_name, str.join(", ", data.keys()), str.join(", ", values))
			conn.execute(sql_statement, data)
		else:
			# TODO: handle the error more gracefully.
			print("Please give fields in order to create.")

	@db_factory_func()
	def find(conn, self, query="", limit=0, sort_by="", return_cols=[]):
		selected_cols = "*"
		if len(return_cols) > 0:
			selected_cols = []
			for col in return_cols:
				if self.fields.get(col) is not None:
					selected_cols.append(col)
				else:
					print("%s is not a valid column name!" % col)
			if len(selected_cols) > 0:
				selected_cols = str.join(",", selected_cols)
			else:
				# TODO: handle the error elegantly.
				print("There is no valid column name!")
				selected_cols = "*"
		sql_statement = "SELECT {} FROM {} ".format(selected_cols, self.table_name)
		if len(query) > 0:
			sql_statement += " WHERE {} ".format(query)
		if limit > 0:
			sql_statement += " LIMIT {} ".format(limit)
		if len(sort_by) > 0 and self.fields.get(sort_by) is not None:
			sql_statement += " ORDER BY {} ".format(sort_by)
		return conn.execute(sql_statement)

	def find_one(self, query=""):
		return self.find(query, limit=1)

	def find_by_id(self, _id):
		return self.find_one("id=%s" % _id)

	@db_factory_func()
	def update(conn, self, data, query="", returning_id=True):
		sql_statement = "UPDATE {} SET ".format(self.table_name)

		values = []
		for field in data:
			if self.fields.get(field) is not None:
				values.append("{}=%({})s".format(field, field))
		sql_statement += str.join(", ", values)

		if len(query) > 0:
			sql_statement += " WHERE {} ".format(query)

		if returning_id:
			sql_statement += "RETURNING id"

		return conn.execute(sql_statement, data)

	def update_by_id(self, _id, data):
		return self.update(data, query=("id='%s'" % _id))

	@db_factory_func()
	def delete(conn, self, query="", returning_id=True):
		sql_statement = "DELETE FROM {} ".format(self.table_name)
		if len(query) > 0:
			sql_statement += " WHERE {} ".format(query)
		else:
			sql_statement += "* "
		if returning_id:
			sql_statement += "RETURNING id"
		return conn.execute(sql_statement)

	def delete_by_id(self, _id):
		return self.delete(query=("id=%s" % _id))
