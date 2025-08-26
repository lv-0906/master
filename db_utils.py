from config import get_db_connection


def is_value_exists(table,column,value):
    """
    检查指定表中是否存在指定列的值
    :param table: 表名
    :param column: 列名
    :param value: 值
    :return: 如果存在则返回True，否则返回False
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT count(*) FROM {table} WHERE {column} = %s"
    cursor.execute(query, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0
