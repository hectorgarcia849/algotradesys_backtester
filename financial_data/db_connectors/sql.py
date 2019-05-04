import mysql.connector


class AlgoTradeDBSQL:

    def __init__(self):
        self.connector = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="algotradedb"
        )
        self.cursor = self.connector.cursor()

    def getDataFrom(self, table_name, n_days):
        query = 'SELECT adj_close_price FROM {} LIMIT {};'.format(table_name, n_days)
        self.cursor.execute(query)
        return self.cursor.fetchall()







