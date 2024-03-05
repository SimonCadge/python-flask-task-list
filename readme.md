# Python Flask Task API
This is my Task REST API, written in Python Flask and based on the problem definition found in problem-definition.md.  
I have also added an Nginx reverse-proxy and the Flask-Migrate package for database migrations.  

### DigitalOcean Hosted Address
I'm hosting the API on a DigitalOcean droplet based in Sydney.  
The ip address is http://170.64.218.21, and you can use the requests defined in `prod-scratch.http` to test it.  

### Running
I have used Docker throughout development and deployment, so ensure you have Docker and Docker Compose installed.  
**Tests:**  
`docker compose --profile test --env-file .env.dev up --build`  
**Dev deployment:**  
`docker compose --profile dev --env-file .env.dev up --build`  
**Prod deployment:**  
`docker compose --profile prod --env-file .env.dev up --build`   
*Currently dev and prod profiles are the same, but in a more complex project there would be differences (e.g. using RDS so removing the db service in prod)*

### Features
 - Python 3.12.2 and Flask 3.0.2
 - Flask app, Postgres database and Nginx reverse-proxy all containerised
 - Docker compose yml defined with profiles seperating test, dev and prod
 - Flask-Migrate used to automatically prepare the db on first deployment and ensure the db and code remain in sync
 - entrypoint.sh runs `flask db upgrade` before every deployment whether test, dev or prod
 - Task model defined in `models/task.py` to control database table definition and Flask-SQLAlchemy integration
 - Routes defined in `project/__init__.py` to enable GET, POST, PUT and DELETE requests with proper error handling
 - pytest tests defined in `tests/test_tasks.py` to test happy paths and all potential errors
 - Two part Dockerfile which builds python wheels in the builder stage to keep the final stage as lean as possible
 - Docker images all using Alpine variants, ensuring they only contain exactly what they need to
 - Prod deployment running live at http://170.64.218.21

### Note:
 - I used Flask 3.0.2, not 2.0.x. I believe the difference is negligible, and I'll happily rewrite it in 2.0.x if you like, but in a greenfield project I prefer to use up to date software.
 - In the PUT /task/<id> endpoint the id is specified twice, once as a route parameter and once as a json parameter in the request body. I am treating the route parameter as definitive and I ignore the json parameter.