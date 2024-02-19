from flask_app.config.mysqlconnection import connectToMySQL

db = 'girl_scout_cookies'

class Cookies:
    def __init__(self, data):
        self.id = data['id']
        self.cookie_type = data['cookie_type']
        self.quantity = data['quantity']

    @classmethod
    def create_cookie_order(cls, user_id, cookie_type, quantity):
        query = """
            INSERT INTO cookies (user_id, cookie_type, quantity)
            VALUES (%(user_id)s, %(cookie_type)s, %(quantity)s)
        """
        data = {
        'user_id': user_id,
        'cookie_type': cookie_type,
        'quantity': quantity
    }
        cookie_id = connectToMySQL(db).query_db(query, data)
        new_cookie = cls({
        'id': cookie_id,
        'user_id': user_id,
        'cookie_type': cookie_type,
        'quantity': quantity
    })
        return new_cookie

    @classmethod
    def get_cookies(cls, user_id):
        query = """
            SELECT cookies.id, cookies.cookie_type, cookies.quantity
            FROM users
            LEFT JOIN cookies ON users.id = cookies.user_id
            WHERE users.id = %(user_id)s
        """
        data = {'user_id': user_id}
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_order_by_id(cls, order_id):
        query = "SELECT * FROM cookies WHERE id = %(order_id)s"
        data = {'order_id': order_id}
        result = connectToMySQL('girl_scout_cookies').query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def update_order(cls, order_id, cookie_type, quantity):
        query = """
            UPDATE cookies
            SET cookie_type = %(cookie_type)s, quantity = %(quantity)s
            WHERE id = %(order_id)s
        """
        data = {'order_id': order_id, 'cookie_type': cookie_type, 'quantity': quantity}
        return connectToMySQL('girl_scout_cookies').query_db(query, data)
