from oracle_operator import OracleOperator, CursorProxy
import oracledb
import petl as etl


# import cx_Oracle

db_operator = OracleOperator("config.yaml")

connection = db_operator.get_conn()
cursor = db_operator.get_cursor()


# for row in cursor.execute("select sysdate from dual"):
#     print(row)
#
# cursor.execute("""
#     declare
#         dummy SYS_REFCURSOR;
#         var1    NUMBER;
#     begin
#         dbms_output.put_line('{}');
#     end;
# """.format(1234))
#
# text_var = cursor.var(str)
# status_var = cursor.var(int)
# while True:
#     cursor.callproc("dbms_output.get_line", (text_var, status_var))
#     if status_var.getvalue() != 0:
#         print(status_var.getvalue())
#         break
#     print(text_var.getvalue())

def get_cursor():
    return CursorProxy(connection.cursor())


table = etl.fromdb(connection, 'select * from rghosh.persons')

print(table)

etl.todb(table, get_cursor(), 'rghosh.test1', dialect='oracle', create=False, commit=True)
