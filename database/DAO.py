from database.DB_connect import DBConnect
from model.customers import Customer


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_customers(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct c.*
        from customers c, orders o, stores s
        where o.customer_id = c.customer_id  
        and s.store_id = o.store_id
        and s.store_id = %s
        """
        cursor.execute(query, (store,))

        for row in cursor:
            print(row)
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results

if __name__ == '__main__':
    DAO = DAO()
    print(DAO.get_customers(DAO))