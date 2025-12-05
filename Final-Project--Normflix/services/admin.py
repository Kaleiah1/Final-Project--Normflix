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

def create_plan(data):
    plan_id = str(uuid.uuid4())
    name = data.get("name")
    max_profiles = data.get("max_profiles")
    price = data.get("price")

    if not name or max_profiles is None or price is None:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO subscription_plan (plan_id, plan_name, max_profiles, price) VALUES (%s,%s,%s,%s)",
        (plan_id, name, max_profiles, price)
    )

    conn.commit()
    conn.close()

    return jsonify({"plan_id": plan_id})

def update_plan(plan_id, data):
    max_profiles = data.get("max_profiles")
    price = data.get("price")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE subscription_plan SET max_profiles=%s, price=%s WHERE plan_id=%s",
        (max_profiles, price, plan_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "The plan was updated successfully!"})

def add_movie(data):
    content_id = str(uuid.uuid4())
    title = data.get("title")
    duration = data.get("duration")
    release_year = data.get("release_year")

    if not title or duration is None or release_year is None:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO content (content_id, title, type, duration, release_year) VALUES (%s,%s,'movie',%s,%s)",
        (content_id, title, duration, release_year)
    )

    conn.commit()
    conn.close()

    return jsonify({"movie_id": content_id})

def add_episode(data):
    content_id = str(uuid.uuid4())
    title = data.get("title")
    duration = data.get("duration")
    release_year = data.get("release_year")
    series_title = data.get("series_title")
    season_no = data.get("season_no")

    if not title or not series_title or duration is None or release_year is None or season_no is None:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO content (content_id, title, type, duration, release_year) VALUES (%s,%s,'episode',%s,%s)",
        (content_id, title, duration, release_year)
    )

    cur.execute(
        "INSERT INTO episode_info (content_id, series_title, season_no) VALUES (%s,%s,%s)",
        (content_id, series_title, season_no)
    )

    conn.commit()
    conn.close()

    return jsonify({"episode_id": content_id})

def create_genre(data):
    genre_id = str(uuid.uuid4())
    name = data.get("genre_name")

    if not name:
        return jsonify({"error": "Missing genre_name"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO genre (genre_id, name) VALUES (%s,%s)",
        (genre_id, name)
    )

    conn.commit()
    conn.close()

    return jsonify({"genre_id": genre_id})

def assign_genre(data):
    content_id = data.get("content_id")
    genre_id = data.get("genre_id")

    if not content_id or not genre_id:
        return jsonify({"error": "Missing content_id or genre_id"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO content_genre (content_id, genre_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
        (content_id, genre_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Genre assigned"})

def add_video_file(data):
    file_id = str(uuid.uuid4())
    content_id = data.get("content_id")
    duration = data.get("duration")
    resolution = data.get("resolution")
    language = data.get("language")
    file_path = data.get("file_path")

    if not content_id or not duration or not resolution or not language or not file_path:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO video_file (file_id, content_id, duration, resolution, language, file_path) VALUES (%s,%s,%s,%s,%s,%s)",
        (file_id, content_id, duration, resolution, language, file_path)
    )

    conn.commit()
    conn.close()

    return jsonify({"file_id": file_id})
