import psycopg2
import uuid
from flask import jsonify

def get_db():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="normflix",
        user="normadmin",
        password="normpass"
    )

def create_profile(account_id, data):
    profile_name = data.get("profile_name")
    age_restrict = data.get("age_restrict")

    if profile_name is None or age_restrict is None:
        return jsonify({"error": "You are still missin information for the required fields."}), 400

    profile_id = str(uuid.uuid4())

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_profile (profile_id, account_id, profile_name, age_restrict) VALUES (%s,%s,%s,%s)",
        (profile_id, account_id, profile_name, age_restrict)
    )
    conn.commit()
    conn.close()

    return jsonify({"profile_id": profile_id, "message": "Profile created!"}), 201


def get_profiles(account_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT profile_id, profile_name, age_restrict FROM user_profile WHERE account_id=%s",
        (account_id,)
    )
    rows = cur.fetchall()
    conn.close()

    profiles = []
    for r in rows:
        profiles.append({
            "profile_id": r[0],
            "profile_name": r[1],
            "age_restrict": r[2]
        })

    return jsonify(profiles)


def update_profile(profile_id, account_id, data):
    profile_name = data.get("profile_name")
    age_restrict = data.get("age_restrict")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT account_id FROM user_profile WHERE profile_id=%s",
        (profile_id,)
    )
    owner = cur.fetchone()

    if not owner or owner[0] != account_id:
        conn.close()
        return jsonify({"error": "Unauthorized"}), 403

    cur.execute(
        "UPDATE user_profile SET profile_name=%s, age_restrict=%s WHERE profile_id=%s",
        (profile_name, age_restrict, profile_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Your profile was updated successfully!"})


def delete_profile(profile_id, account_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT account_id FROM user_profile WHERE profile_id=%s",
        (profile_id,)
    )
    owner = cur.fetchone()

    if not owner or owner[0] != account_id:
        conn.close()
        return jsonify({"error": "Unauthorized"}), 403

    cur.execute("DELETE FROM user_profile WHERE profile_id=%s", (profile_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Profile deleted successfully"})
