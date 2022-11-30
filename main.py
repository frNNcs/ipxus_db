import os
import mysql.connector
from dotenv import load_dotenv
from matplotlib import pyplot as plt


load_dotenv()

def main():
    with mysql.connector.connect(
        user= os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DATABASE')
    ) as connection:
        with connection.cursor() as cursor:
            # get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            tables = [t[0] for t in tables if t[0] != 'users']
            # get table sizes
            tables_ordered_list = []
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                tables_ordered_list.append((count, table))
            # remove tables with 0 rows
            tables_ordered_list = [t for t in tables_ordered_list if t[0] != 0]
            # sort by count
            tables_ordered_list.sort(reverse=True)

            # top 20
            tables_ordered_list = tables_ordered_list[:20]

            # save png file plt bar chart
            plt.bar([t[1] for t in tables_ordered_list], [t[0] for t in tables_ordered_list])
            plt.xticks(rotation=90)
            plt.savefig('tables.png', bbox_inches='tight')

if __name__ == "__main__":
    main()
