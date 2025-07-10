from database.DB_connect import DBConnect
from model.customers import Customer

class Product:
    pass


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_nodes(store):
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
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results
    
    @staticmethod
    def get_edges(idMap, product = None):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT
            o1.customer_id    AS customer_a,
            o2.customer_id   AS customer_b,
            COUNT(DISTINCT oi1.product_id) AS shared_products
        FROM orders o1,
             order_items oi1,
             orders o2,
             order_items oi2
        WHERE o1.order_id    = oi1.order_id
          AND o2.order_id    = oi2.order_id
          AND oi1.product_id = oi2.product_id     -- hanno comprato lo stesso prodotto
          AND o1.customer_id < o2.customer_id   -- evita doppioni e self‐loop
          AND oi1.product_id = COALESCE(%s, oi1.product_id)
        GROUP BY
            o1.customer_id,
            o2.customer_id
        ;
        """
        cursor.execute(query, (product,))

        for row in cursor:
            results.append((idMap[row["customer_a"]],idMap[row["customer_b"]], row["shared_products"]))

        cursor.close()
        conn.close()
        return results

if __name__ == '__main__':
    DAO = DAO()
    prova = DAO.get_nodes(1)
    for p in prova:
        print(p)