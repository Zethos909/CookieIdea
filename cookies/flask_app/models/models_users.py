from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_cookies import Cookies

db = 'girl_scout_cookies'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cookies = [Cookies(cookie_data) for cookie_data in data.get('cookies', [])]

    @classmethod
    def get_all_orders(cls):
        query = """
            SELECT user.id AS user_id, user.name AS user_name,
                   cookies.id AS cookie_id, cookies.cookie_type, cookies.quantity
            FROM user
            LEFT JOIN cookies ON user.id = cookies.user_id
        """
        orders_data = connectToMySQL(db).query_db(query)

        orders_by_user = {}
        for order_data in orders_data:
            user_id = order_data['user_id']
            if user_id not in orders_by_user:
                orders_by_user[user_id] = {
                    'id': user_id,
                    'name': order_data['user_name'],
                    'created_at': None,
                    'updated_at': None,
                    'cookies': []
                }
            cookie_info = {
                'id': order_data['cookie_id'],
                'cookie_type': order_data['cookie_type'],
                'quantity': order_data['quantity']
            }
            orders_by_user[user_id]['cookies'].append(cookie_info)

        orders = [cls(order_info) for order_info in orders_by_user.values()]
        return orders

    @classmethod
    def create_cookie_order(cls, user_id, cookie_type, quantity):
        query = """
            INSERT INTO cookies (user_id, cookie_type, quantity, created_at, updated_at)
            VALUES (%(user_id)s, %(cookie_type)s, %(quantity)s, NOW(), NOW());
            INSERT INTO user (name, created_at, updated_at)
            VALUES (%(user_name)s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE name=VALUES(name);
        """
        data = {
            'user_id': user_id,
            'cookie_type': cookie_type,
            'quantity': quantity,
            'user_name': None  # Provide a default value to avoid KeyErrors
        }
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_user_by_name(cls, user_name):
        query = "SELECT * FROM user WHERE name = %(user_name)s"
        data = {'user_name': user_name}
        result = connectToMySQL(db).query_db(query, data)

        if result:
            return cls(result[0])
        else:
            return None
