from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # If you have a password, enter it here
    database="athlex_db"
)
cursor = db.cursor()

# ✅ FIX 1: Define the Home Route Properly
@app.route('/')
def home():
    return "AthleX API is Running Successfully!"

# ✅ FIX 2: Register get_user() as a Separate Route
@app.route('/get_user', methods=['GET'])
def get_user():
    name = request.args.get('name')
    sql = "SELECT * FROM users WHERE name = %s"
    cursor.execute(sql, (name,))
    result = cursor.fetchone()
    if result:
        return jsonify({
            "name": result[1],
            "age": result[2],
            "gender": result[3],
            "height": result[4],
            "weight": result[5],
            "goal": result[6],
            "diet": result[7],
            "workout": result[8],
            "medical": result[9]
        })
    return jsonify({"message": "User not found"})

# ✅ FIX 3: Ensure /add_user Route Works
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    sql = "INSERT INTO users (name, age, gender, height, weight, fitness_goal, diet_preference, workout_type, medical_conditions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data['name'], data['age'], data['gender'], data['height'], data['weight'], data['goal'], data['diet'], data['workout'], data['medical'])
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "User added successfully!"})

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
