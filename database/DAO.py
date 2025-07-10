from database.DB_connect import DBConnect

from model.order import Order
class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct s.store_id as store, s.store_name as name from stores s"

        cursor.execute(query)

        for row in cursor:
            print(row)
            results.append((row["store"], row["name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOrdersbyStore(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct * from orders o where o.store_id=%s"""

        cursor.execute(query, (store,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """Select DISTINCT o1.order_id as id1, o2.order_id as id2, count(oi.quantity+ oi2.quantity) as cnt
                from orders o1, orders o2, order_items oi, order_items oi2 
                where o1.store_id=%s
                and o1.store_id=o2.store_id 
                and o1.order_date > o2.order_date
                and oi.order_id = o1.order_id
                and oi2.order_id  = o2.order_id
                and DATEDIFF(o1.order_Date, o2.order_date) < %s
                group by o1.order_id, o2.order_id	"""

        cursor.execute(query, (store,k))

        for row in cursor:
            results.append((idMap[row["id1"]],idMap[row["id2"]], row["cnt"]))


        cursor.close()
        conn.close()

        return results

if __name__ == '__main__':
    DAO = DAO()
    stores = DAO.getAllStores()