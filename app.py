from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("tovo.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

# Get all items
@app.route("/items", methods=["GET"])
def get_items():
    conn = sqlite3.connect("tovo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "name": r[1], "description": r[2], "price": r[3], "stock": r[4]} 
        for r in rows
    ])

# Create item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    conn = sqlite3.connect("tovo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, description, price, stock) VALUES (?, ?, ?, ?)", 
                (data["name"], data.get("description", ""), data["price"], data["stock"]))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({
        "id": new_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "price": data["price"],
        "stock": data["stock"]
    }), 201

# Update item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    conn = sqlite3.connect("tovo.db")
    cur = conn.cursor()
    cur.execute("UPDATE items SET name=?, description=?, price=?, stock=? WHERE id=?", 
                (data["name"], data.get("description", ""), data["price"], data["stock"], item_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item updated successfully"})

# Delete item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = sqlite3.connect("tovo.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
