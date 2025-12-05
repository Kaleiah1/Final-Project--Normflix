import psycopg2
import uuid
import hashlib
from flask import jsonify
from datetime import date

def get_db():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="normflix",
        user="normadmin",
        password="normpass"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return str(uuid.uuid4())

def register_user(data):
    email = data.get("email")
    password = data.get("password")
    plan_id = data.get("plan_id")

    if not email or not password or not plan_id:
        return jsonify({"error": "You are still missin information for the required fields."}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT email FROM user_account WHERE email=%s", (email,))
    if cur.fetchone():
        conn.close()
        return jsonify({"error": "The email enter is already registered to an account"}), 400

    account_id = str(uuid.uuid4())
    hashed = hash_password(password)
    creation = date.today()

    cur.execute(
        "INSERT INTO user_account (account_id, plan_id, email, password, creation_date) VALUES (%s,%s,%s,%s,%s)",
        (account_id, plan_id, email, hashed, creation)
    )

    conn.commit()
    conn.close()

    return jsonify({"account_id": account_id, "message": "You're registration successful!"}), 201


def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Your missing email or password"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT account_id, password FROM user_account WHERE email=%s", (email,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Sorry, account not found"}), 404

    account_id, stored_hash = row

    if stored_hash != hash_password(password):
        conn.close()
        return jsonify({"error": "Incorrect password"}), 401

    token = generate_token()

    cur.execute("UPDATE user_account SET auth_token=%s WHERE account_id=%s", (token, account_id))
    conn.commit()
    conn.close()

    return jsonify({"account_id": account_id, "auth_token": token}), 200


def get_account_info(account_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT ua.account_id, ua.email, sp.plan_name, sp.max_profiles, sp.price
        FROM user_account ua
        JOIN subscription_plan sp ON ua.plan_id = sp.plan_id
        WHERE ua.account_id=%s
    """, (account_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Sorry, this account was not found."}), 404

    return jsonify({
        "account_id": row[0],
        "email": row[1],
        "subscription": {
            "plan_name": row[2],
            "max_profiles": row[3],
            "price": float(row[4])
        }
    })
