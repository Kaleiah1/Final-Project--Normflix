import requests

BASE_URL = "http://127.0.0.1:5000"

def main():
    plan_resp = requests.post(
        f"{BASE_URL}/api/admin/plans",
        json={
            "name": "Standard Admin Plan",
            "max_profiles": 4,
            "price": 15.99
        }
    )
    print("Create Plan status:", plan_resp.status_code)
    print("Create Plan body:", plan_resp.text)

    if plan_resp.status_code != 200 and plan_resp.status_code != 201:
        return  # stop if plan creation failed

    data = plan_resp.json()
    plan_id = data.get("plan_id")

    genre_resp = requests.post(
        f"{BASE_URL}/api/admin/genres",
        json={"genre_name": "Action"}
    )
    print("Create Genre status:", genre_resp.status_code)
    print("Create Genre body:", genre_resp.text)

    if genre_resp.status_code != 200 and genre_resp.status_code != 201:
        return

    genre_id = genre_resp.json().get("genre_id")

    movie_resp = requests.post(
        f"{BASE_URL}/api/admin/content/movie",
        json={
            "title": "Admin Demo Movie",
            "duration": "01:35:00",
            "release_year": 2024
        }
    )
    print("Add Movie status:", movie_resp.status_code)
    print("Add Movie body:", movie_resp.text)
    if movie_resp.status_code != 200 and movie_resp.status_code != 201:
        return

    movie_id = movie_resp.json().get("movie_id")

    assign_resp = requests.post(
        f"{BASE_URL}/api/admin/content/genre",
        json={
            "content_id": movie_id,
            "genre_id": genre_id
        }
    )
    print("Assign Genre status:", assign_resp.status_code)
    print("Assign Genre body:", assign_resp.text)

    video_resp = requests.post(
        f"{BASE_URL}/api/admin/video",
        json={
            "content_id": movie_id,
            "duration": "01:35:00",
            "resolution": "1080p",
            "language": "English",
            "file_path": "/videos/admin-demo-movie.mp4"
        }
    )
    print("Add Video File status:", video_resp.status_code)
    print("Add Video File body:", video_resp.text)

if __name__ == "__main__":
    main()
