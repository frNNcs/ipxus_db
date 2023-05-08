import os
import mysql.connector
from dotenv import load_dotenv
from matplotlib import pyplot as plt


load_dotenv()

# Lista de 6 colores de frio a calido partiendo del azul al rojo
COLORS = [
    '#6495ED',
    '#7FFFD4',
    '#00FF7F',
    '#ADFF2F',
    '#FFFF00',
    '#FF0000'
]

def main():
    with mysql.connector.connect(
        user= os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DATABASE')
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            tables = [table[0] for table in tables]

            tables_ordered_list = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]

                cursor.execute(f"SHOW COLUMNS FROM {table}")
                columns = cursor.fetchall()
                columns = [column[0] for column in columns]

                tables_ordered_list[table] = {
                    'count': count,
                    'columns': columns
                }
            # obtener el numero de tablas mas grande
            max_tables = max(tables_ordered_list.values(), key=lambda x: x['count'])['count']
            # dividir en 6 partes
            step = max_tables / 6


            # crear grafico de las relaciones entre tablas utilizando pygraphviz
            import pygraphviz as pgv
            G = pgv.AGraph(directed=True)
            G.graph_attr['rankdir'] = 'LR'
            G.node_attr['shape'] = 'box'
            G.node_attr['style'] = 'filled'
            G.node_attr['fillcolor'] = '#6495ED'
            G.node_attr['fontcolor'] = 'white'
            G.node_attr['fontsize'] = '12'
            G.edge_attr['color'] = '#6495ED'

            # Recorrer todas las tablas y graficar sus relaciones
            for table, keys in tables_ordered_list.items():
                if keys is not None:
                    count, columns = keys.values()
                    color_order = int(int(count) / step) -1
                    if color_order < 0:
                        color_order = 0
                    table_color = COLORS[color_order]
                    G.add_node(table, fillcolor=table_color, color=table_color)
                    for column in columns:
                        if column.endswith('_id'):
                            # get the table name from the column name
                            related_table = column.replace('_id', '')
                            # si existe la tabla relacionada, agregar el nodo, la relacion y sacarlo del diccionario
                            # tables_with_columns
                            if related_table in tables_ordered_list.keys():
                                G.add_node(related_table)
                                G.add_edge(related_table, table)
                                tables_ordered_list[related_table] = None

            G.layout(prog='dot')
            G.draw('graph.png')


if __name__ == "__main__":
    main()
