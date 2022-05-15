![Yamdb workflow](https://github.com/ai-zaytsev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# My API project
## Project is aimed to accumulate users' reviews on different subjects
### Stack used: 
- Python
- Django

### Setup instructions:
1. Install docker: https://docs.docker.com/engine/install/ubuntu/

2. Clone 
```
docker pull aizaytsev/api_yamdb
```

3. Configure .git:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=*YOUR_SECRET_KEY*
```# yamdb_final# yamdb_final
yamdb_final
yamdb_final

4. Build
```
docker-compose up -d --build
```

5. Migrate, create superiser, collect static
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

6. Go to http://localhost/


*Authors*: Alex, Alexander, Ilya 

