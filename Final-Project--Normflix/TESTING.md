step 1: 
start the postgres databse using the command:

docker start normflix_pg

expected to see:
"Database schema created successfully!"
step 2: 
start Flask:

python app.py

expected to run:
http://127.0.0.1:5000

step 3:
test the admin demo script to check: making a plan, genre, adding a movie, assigning a specific genre, adding video files

python scripts/admin_demo.py

200 means the script ran sucessfully

step 4:
test the user features to check: user registration, creating profiles, logging on, adding movies, listing movies, wishlist, viewing history

python scripts/user_demo.py

200(1) means the script ran sucessfully

step 5(optional):
if you want to double check the database, use the command:

docker exec -it normflix_pg psql -U normadmin -d normflix

and then:

SELECT * FROM subscription_plan;
SELECT * FROM user_account;
SELECT * FROM content;

once finished using te 
end:
