import sqlite3;

connection = sqlite3.connect('database/storage/users.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

def prepare_value(value):
    return f"'{value}'" if isinstance(value, str) else str(value)

def join_array(array):
    result = []
    for item in array:
        item = prepare_value(item)
        result.append(item)

    return ','.join(result)

def select(table_name, columns, values):
    query = f'select * from {table_name} '
    params = ''
    for index, column in enumerate(columns):
        if index < 1:
            params += 'where '
        else:
            params += ' and '
        params += f'{column} = {prepare_value(values[index])}'
    cursor.execute(query + params)
    return cursor.fetchall()

def insert(table_name, columns, values):
    print(f'insert into {table_name} ({join_array(columns)}) values ({join_array(values)})')
    cursor.execute(f'insert into {table_name} ({join_array(columns)}) values ({join_array(values)})')
    connection.commit()

def update(table_name, set, where):
    cursor.execute(f'update {table_name} set {set["column"]} = {prepare_value(set["value"])} where {where["column"]} = {prepare_value(where["value"])}')
    connection.commit()

def delete(table_name, colunm, value):
    cursor.execute(f'delete from {table_name} where {colunm} = {prepare_value(value)}')
    connection.commit()

def selectMusicByUserId(user_id):
    cursor.execute(f'SELECT * FROM music left join users_music as um on id = um.music_id where user_id = {prepare_value(user_id)}')
    return cursor.fetchall()