import psycopg2

schema_sql = """
CREATE TABLE subscription_plan(
    plan_id VARCHAR(50) PRIMARY KEY,
    plan_name TEXT NOT NULL,
    max_profiles INTEGER NOT NULL,
    price NUMERIC(4,2) NOT NULL
);

CREATE TABLE user_account(
    account_id VARCHAR(50)  PRIMARY KEY,
    plan_id VARCHAR(50) NOT NULL REFERENCES subscription_plan(plan_id),
    email TEXT NOT NULL UNIQUE,
    password TEST NOT NULL,
    auth_token TEXT,
    creation_date DATE NOT NULL
);

CREATE TABLE user_profile(
    profile_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL REFERENCES user_account(account_id),
    profile_name TEXT NOT NULL,
    age_restrict BOOLEAN NOT NULL
);

CREATE TABLE content(
    content_id VARCHAR(50) PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    duration TIME NOT NULL,
    release_year INT NOT NULL
);

CREATE TABLE episode_info(
    content_id VARCHAR(50) PRIMARY KEY REFERENCES content(content_id),
    series_title TEXT NOT NULL,
    season_no INT NOT NULL
);

CREATE TABLE genre(
    genre_id VARCHAR(50) PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE content_genre(
    content_id VARCHAR(50) NOT NULL REFERENCES content(content_id),
    genre_id VARCHAR(50) NOT NULL REFERENCES genre(genre_id),
    PRIMARY KEY (content_id, genre_id)
);

CREATE TABLE video_file(
    file_id VARCHAR(50) PRIMARY KEY,
    content_id VARCHAR(50) NOT NULL REFERENCES content(content_id),
    duration TIME NOT NULL,
    resolution TEXT NOT NULL,
    language TEXT NOT NULL,
    file_path TEXT NOT NULL
);

CREATE TABLE wishlist(
    profile_id VARCHAR(50) NOT NULL REFERENCES user_profile(profile_id),
    content_id VARCHAR(50) NOT NULL REFERENCES content(content_id),
    PRIMARY KEY (profile_id, content_id)
);

CREATE TABLE viewing_history(
    profile_id VARCHAR(50) NOT NULL REFERENCES user_profile(profile_id),
    content_id VARCHAR(50) NOT NULL REFERENCES content(content_id),
    timestamp TIME NOT NULL,
    PRIMARY KEY (profile_id, content_id, timestamp)
);
"""

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="normflix",
        user="normadmin",
        password="normpass"
    )
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Database schema created successfully!")
except Exception as e:
    print("Error creating database schema:")
    print(e)
