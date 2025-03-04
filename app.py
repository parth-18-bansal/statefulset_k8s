from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection details
MYSQL_PRIMARY = os.getenv("MYSQL_PRIMARY", "mysql-0.mysql")
MYSQL_REPLICAS = os.getenv("MYSQL_REPLICA", "mysql-1.mysql,mysql-2.mysql").split(",")

def get_db_connection(primary=True):
    """Connects to MySQL primary for writes and replicas for reads."""
    host = MYSQL_PRIMARY if primary else MYSQL_REPLICAS[0]
    return mysql.connector.connect(
        host=host,
        user="root",
        password="rootpassword",
        database="mydb"
    )

@app.route("/write", methods=["POST"])
def write_data():
    data = request.json.get("data", "default")
    conn = get_db_connection(primary=True)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test (name) VALUES (%s)", (data,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Data inserted!"})

@app.route("/read", methods=["GET"])
def read_data():
    conn = get_db_connection(primary=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
