import petl as etl
from oracle_operator import OracleOperator, CursorProxy

db_operator = OracleOperator("config.yaml")

connection = db_operator.get_conn()
cursor = db_operator.get_cursor()


def get_cursor():
    return CursorProxy(connection.cursor())


table = etl.fromdb(connection, 'select * from rghosh.persons')

print(table)

etl.todb(table, get_cursor(), 'rghosh.test1', dialect='oracle', create=False, commit=True)
