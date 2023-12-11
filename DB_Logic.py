from flask import Flask, jsonify, request
import pymysql
import pymysql.cursors

app = Flask(__name__)

# Database connection info
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Send20fire100apple',
    'db': 'IMS',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection

#Read all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM Customers"
        cursor.execute(sql)
        result = cursor.fetchall()
    connection.close()
    return jsonify(result)

#Create new customer
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO Customers (FirstName, LastName, DateOfBirth, Gender, Email, PhoneNumber, Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['FirstName'], data['LastName'], data['DateOfBirth'], data['Gender'], data['Email'], data['PhoneNumber'], data['Address']))
    connection.commit()
    connection.close()
    return jsonify({'status': 'success'})

#Read Single customer with id 
@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM Customers WHERE CustomerID = %s"
        cursor.execute(sql, (customer_id,))
        result = cursor.fetchone()
    connection.close()
    return jsonify(result)

#Update customer with id
@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "UPDATE Customers SET FirstName = %s, LastName = %s, DateOfBirth = %s, Gender = %s, Email = %s, PhoneNumber = %s, Address = %s WHERE CustomerID = %s"
        cursor.execute(sql, (data['FirstName'], data['LastName'], data['DateOfBirth'], data['Gender'], data['Email'], data['PhoneNumber'], data['Address'], customer_id))
    connection.commit()
    connection.close()
    return jsonify({'status': 'success'})

#Delete customer with id
@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM Customers WHERE CustomerID = %s"
        cursor.execute(sql, (customer_id,))
    connection.commit()
    connection.close()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
