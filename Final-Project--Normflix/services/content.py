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


def list_movies():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT content_id, title, release_year, duration FROM content WHERE type='movie'"
    )
    rows = cur.fetchall()
    conn.close()

    movies = []
    for r in rows:
        movies.append({
            "content_id": r[0],
            "title": r[1],
            "release_year": r[2],
            "duration": str(r[3])
        })

    return jsonify(movies)

def get_movie_details(content_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT title, release_year, duration FROM content WHERE content_id=%s AND type='movie'",
        (content_id,)
    )
    movie = cur.fetchone()

    if not movie:
        conn.close()
        return jsonify({"error": "Movie not found"}), 404

    cur.execute(
        "SELECT name FROM genre g JOIN content_genre cg ON g.genre_id=cg.genre_id WHERE cg.content_id=%s",
        (content_id,)
    )
    genres = [row[0] for row in cur.fetchall()]

    cur.execute(
        "SELECT resolution, language, file_path FROM video_file WHERE content_id=%s",
        (content_id,)
    )
    files = []
    for f in cur.fetchall():
        files.append({
            "resolution": f[0],
            "language": f[1],
            "path": f[2]
        })
    conn.close()
    return jsonify({
        "title": movie[0],
        "release_year": movie[1],
        "duration": str(movie[2]),
        "genres": genres,
        "files": files
    })

def add_to_wishlist(account_id, data):
    profile_id = data.get("profile_id")
    content_id = data.get("content_id")

    if not profile_id or not content_id:
        return jsonify({"error": "Missing profile_id or content_id"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT profile_id FROM user_profile WHERE profile_id=%s AND account_id=%s",
        (profile_id, account_id)
    )
    if not cur.fetchone():
        conn.close()
        return jsonify({"error": "This is an unauthorized profile"}), 403
    cur.execute(
        "INSERT INTO wishlist (profile_id, content_id) VALUES (%s,%s) ON CONFLICT DO NOTHING",
        (profile_id, content_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Added to your wishlist"}), 201

def get_wishlist(profile_id, account_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT profile_id FROM user_profile WHERE profile_id=%s AND account_id=%s",
        (profile_id, account_id)
    )
    if not cur.fetchone():
        conn.close()
        return jsonify({"error": "This is an unauthorized profile"}), 403

    cur.execute(
        "SELECT c.content_id, c.title FROM wishlist w JOIN content c ON w.content_id=c.content_id WHERE w.profile_id=%s",
        (profile_id,)
    )
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        items.append({
            "content_id": r[0],
            "title": r[1]
        })

    return jsonify(items)

def remove_from_wishlist(profile_id, content_id, account_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT profile_id FROM user_profile WHERE profile_id=%s AND account_id=%s",
        (profile_id, account_id)
    )
    if not cur.fetchone():
        conn.close()
        return jsonify({"error": "This is an unauthorized profile"}), 403

    cur.execute(
        "DELETE FROM wishlist WHERE profile_id=%s AND content_id=%s",
        (profile_id, content_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Removed successfully"})

def save_viewing_progress(account_id, data):
    profile_id = data.get("profile_id")
    content_id = data.get("content_id")
    timestamp = data.get("timestamp")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT profile_id FROM user_profile WHERE profile_id=%s AND account_id=%s",
        (profile_id, account_id)
    )
    if not cur.fetchone():
        conn.close()
        return jsonify({"error": "This is an unauthorized profile"}), 403

    cur.execute(
        "INSERT INTO viewing_history (profile_id, content_id, timestamp) VALUES (%s,%s,%s)",
        (profile_id, content_id, timestamp)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Your progress has been saved"})

def get_continue_watching(profile_id, account_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT profile_id FROM user_profile WHERE profile_id=%s AND account_id=%s",
        (profile_id, account_id)
    )
    if not cur.fetchone():
        conn.close()
        return jsonify({"error": "This is an unauthorized profile"}), 403

    cur.execute(
        "SELECT content_id, timestamp FROM viewing_history WHERE profile_id=%s ORDER BY timestamp DESC LIMIT 5",
        (profile_id,)
    )
    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "content_id": r[0],
            "resume_time": str(r[1])
        })
    return jsonify(result)
