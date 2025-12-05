import requests

BASE_URL = "http://127.0.0.1:5000"

def main():
    plan_resp = requests.post(
        f"{BASE_URL}/api/admin/plans",
        json={
            "name": "User Demo Plan",
            "max_profiles": 2,
            "price": 9.99
        }
    )
    print("Create Plan:", plan_resp.status_code, plan_resp.json())
    plan_id = plan_resp.json().get("plan_id")

    reg_resp = requests.post(
        f"{BASE_URL}/api/accounts/register",
        json={
            "email": "userdemo@gmail.com",
            "password": "DemoPass123",
            "plan_id": plan_id
        }
    )
    print("Register:", reg_resp.status_code, reg_resp.json())

    login_resp = requests.post(
        f"{BASE_URL}/api/accounts/login",
        json={
            "email": "userdemo@gmail.com",
            "password": "DemoPass123"
        }
    )
    print("Login:", login_resp.status_code, login_resp.json())

    token = login_resp.json().get("auth_token")
    headers = {"Authorization": f"Bearer {token}"}

    profile_resp = requests.post(
        f"{BASE_URL}/api/profiles",
        json={
            "profile_name": "Demo Profile",
            "age_restrict": False
        },
        headers=headers
    )
    print("Create Profile:", profile_resp.status_code, profile_resp.text)

    profile_id = profile_resp.json().get("profile_id")

    movie_resp = requests.post(
        f"{BASE_URL}/api/admin/content/movie",
        json={
            "title": "User Demo Movie",
            "duration": "00:45:00",
            "release_year": 2023
        }
    )
    print("Add Movie:", movie_resp.status_code, movie_resp.json())
    movie_id = movie_resp.json().get("movie_id")

    movies_list = requests.get(f"{BASE_URL}/api/content/movies")
    print("List Movies:", movies_list.status_code, movies_list.json())

    wishlist_resp = requests.post(
        f"{BASE_URL}/api/wishlist",
        json={
            "profile_id": profile_id,
            "content_id": movie_id
        },
        headers=headers
    )
    print("Add to Wishlist:", wishlist_resp.status_code, wishlist_resp.json())

    view_save_resp = requests.post(
        f"{BASE_URL}/api/viewing/save",
        json={
            "profile_id": profile_id,
            "content_id": movie_id,
            "timestamp": "00:10:00"
        },
        headers=headers
    )
    print("Save Viewing:", view_save_resp.status_code, view_save_resp.json())

    continue_resp = requests.get(
        f"{BASE_URL}/api/viewing/{profile_id}",
        headers=headers
    )
    print("Continue Watching:", continue_resp.status_code, continue_resp.json())

if __name__ == "__main__":
    main()
