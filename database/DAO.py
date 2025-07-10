from database.DB_connect import DBConnect
from model.customers import Customer
from model.stores import Store
from model.products import Prodotto



class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct s.* from stores s"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductsByStores(store):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)

        query = """
        select distinct p.*
        from stocks s, products p, stores st
        where s.store_id = s.store_id 
        and s.product_id = p.product_id
        and s.store_id = %s
        """
        cursor.execute(query, (store,))

        res = []
        for row in cursor:
            res.append(Prodotto(**row))

        cursor.close()
        cnx.close()
        return res

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
        order by c.customer_id
        """
        cursor.execute(query, (store,))

        for row in cursor:
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results
    
    @staticmethod
    def get_edges(id_map, product = None):
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
            ca = row["customer_a"]
            cb = row["customer_b"]
            # se uno dei due non è nella mappa, salta
            if ca not in id_map or cb not in id_map:
                continue
            u = id_map[ca]
            v = id_map[cb]
            w = row["shared_products"]
            results.append((u, v, w))
        cursor.close()
        conn.close()
        return results

if __name__ == '__main__':
    DAO = DAO()

    DAO.getProductsByStores(1)