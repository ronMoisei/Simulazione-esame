from database.DB_connect import DBConnect
from model.products import Product
from model.stores import Store


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
            print(row)
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getYearsByStores(store):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)

        query = """
        select distinct year(o.order_date) as year
        from orders o, stores s
        where o.store_id = s.store_id
        and s.store_id = %s
        """
        cursor.execute(query, (store,))

        res = []
        for row in cursor:
            print(row)
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res
    @staticmethod
    def get_Products(store, qty):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT 
                p.*
            FROM products      p,
                 stocks        s,
                 stores        st,
                 order_items   oi,
                 orders        o
            WHERE p.product_id = s.product_id
              AND s.store_id   = st.store_id
              AND p.product_id = oi.product_id
              AND oi.order_id  = o.order_id
              AND st.store_id  = %s
            GROUP BY p.product_id
            HAVING SUM(oi.quantity) >= %s
        """
        cursor.execute(query, (store,qty))

        res = []
        for row in cursor:
            res.append(Product(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_EdgesWeight(store, idMap, year = None):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)

        query = """
                SELECT 
                    oi1.product_id AS p,
                    oi2.product_id AS q,
                    COUNT(DISTINCT oi1.order_id) AS weight
                FROM orders o,
                     order_items oi1,
                     order_items oi2
                WHERE o.order_id   = oi1.order_id
                  AND o.order_id   = oi2.order_id
                  AND oi1.product_id < oi2.product_id
                  AND o.store_id   = %s
                  AND YEAR(o.order_date)
                      = COALESCE(%s, YEAR(o.order_date))
                GROUP BY
                    oi1.product_id,
                    oi2.product_id;
        """
        cursor.execute(query, (store, year))

        res = []
        for row in cursor:
            p_id = row['p']
            q_id = row['q']
            if p_id not in idMap or q_id not in idMap:
                # uno dei due non è tra i nodi scelti → skip
                continue
            u = idMap[p_id]
            v = idMap[q_id]
            w = row['weight']
            res.append((u, v, w))

        cursor.close()
        cnx.close()
        return res

if __name__ == '__main__':
    DAO = DAO()
    years = DAO.getYearsByStores(1)
    print(years)