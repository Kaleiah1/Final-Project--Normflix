from flask import Flask, request, jsonify
import psycopg2
import uuid
from datetime import datetime

from services.authen import register_user, login_user, get_account_info
from services.profile import create_profile, get_profiles, update_profile, delete_profile
from services.content import (
    list_movies, get_movie_details,
    add_to_wishlist, get_wishlist, remove_from_wishlist,
    save_viewing_progress, get_continue_watching
)
from services.admin import (
    create_plan, update_plan,
    add_movie, add_episode,
    create_genre, assign_genre,
    add_video_file
)

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="normflix",
        user="normadmin",
        password="normpass"
    )


def require_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Authorization token required"}), 401
        token = token.replace("Bearer ", "").strip()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT account_id FROM user_account WHERE auth_token=%s", (token,))
        result = cur.fetchone()
        conn.close()

        if not result:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.account_id = result[0]
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

@app.post("/api/accounts/register")
def route_register():
    data = request.json
    return register_user(data)

@app.post("/api/accounts/login")
def route_login():
    data = request.json
    return login_user(data)

@app.get("/api/account")
@require_token
def route_get_account():
    return get_account_info(request.account_id)

@app.post("/api/profiles")
@require_token
def route_create_profile():
    data = request.json
    return create_profile(request.account_id, data)

@app.get("/api/profiles")
@require_token
def route_list_profiles():
    return get_profiles(request.account_id)

@app.put("/api/profiles/<profile_id>")
@require_token
def route_update_profile(profile_id):
    data = request.json
    return update_profile(profile_id, request.account_id, data)

@app.delete("/api/profiles/<profile_id>")
@require_token
def route_delete_profile(profile_id):
    return delete_profile(profile_id, request.account_id)

@app.get("/api/content/movies")
def route_get_movies():
    return list_movies()

@app.get("/api/content/movies/<content_id>")
def route_movie_details(content_id):
    return get_movie_details(content_id)

@app.post("/api/wishlist")
@require_token
def route_add_to_wishlist():
    data = request.json
    return add_to_wishlist(request.account_id, data)

@app.get("/api/wishlist/<profile_id>")
@require_token
def route_get_wishlist(profile_id):
    return get_wishlist(profile_id, request.account_id)

@app.delete("/api/wishlist/<profile_id>/<content_id>")
@require_token
def route_remove_from_wishlist(profile_id, content_id):
    return remove_from_wishlist(profile_id, content_id, request.account_id)

@app.post("/api/viewing/save")
@require_token
def route_save_view():
    data = request.json
    return save_viewing_progress(request.account_id, data)

@app.get("/api/viewing/<profile_id>")
@require_token
def route_continue_watching(profile_id):
    return get_continue_watching(profile_id, request.account_id)

@app.post("/api/admin/plans")
def route_create_plan():
    data = request.json
    return create_plan(data)

@app.put("/api/admin/plans/<plan_id>")
def route_update_plan(plan_id):
    data = request.json
    return update_plan(plan_id, data)

@app.post("/api/admin/content/movie")
def route_add_movie():
    data = request.json
    return add_movie(data)

@app.post("/api/admin/content/episode")
def route_add_episode():
    data = request.json
    return add_episode(data)

@app.post("/api/admin/genres")
def route_create_genre():
    data = request.json
    return create_genre(data)

@app.post("/api/admin/content/genre")
def route_assign_genre():
    data = request.json
    return assign_genre(data)

@app.post("/api/admin/video")
def route_video_upload():
    data = request.json
    return add_video_file(data)

if __name__ == "__main__":
    app.run(debug=True)
