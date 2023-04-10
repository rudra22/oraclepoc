# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from OracleOperator import OracleOperator

db_operator = OracleOperator("config.yaml")

connection = db_operator.get_conn()
cursor = db_operator.get_cursor()

# Create a table

cursor.execute("""
    begin
        execute immediate 'drop table todoitem';
        exception when others then if sqlcode <> -942 then raise; end if;
    end;""")

cursor.execute("""
    create table todoitem (
        id number generated always as identity,
        description varchar2(4000),
        creation_ts timestamp with time zone default current_timestamp,
        done number(1,0),
        primary key (id))""")

# Insert some data

rows = [("Task 1", 0),
        ("Task 2", 0),
        ("Task 3", 1),
        ("Task 4", 0),
        ("Task 5", 1)]

cursor.executemany("insert into todoitem (description, done) values(:1, :2)", rows)
print(cursor.rowcount, "Rows Inserted")

connection.commit()

# Now query the rows back
for row in cursor.execute('select description, done from todoitem'):
    if row[1]:
        print(row[0], "is done")
    else:
        print(row[0], "is NOT done")