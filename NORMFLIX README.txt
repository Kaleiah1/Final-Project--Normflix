Setup:
Step 1: Create a docker container on your local machine that you want to use for the database as well as have python installed on your machine.


Step 2: follow these commands in command prompt and the database will be created. A message saying “Database schema created successfully!” will appear if done correctly, an error message if not.


1st command:


docker run -d --name normflix_pg ^
  -e POSTGRES_USER=normadmin ^
  -e POSTGRES_PASSWORD=normpass ^
  -e POSTGRES_DB=normflix ^
  -p 5432:5432 ^
  postgres


2nd command:


cd (insert file path here)


3rd command:


py database_setup.py


Step 3: Verify the tables
1. docker exec -it normflix_pg psql -U normadmin -d normflix
2. \dt
3. \q    (to quit)