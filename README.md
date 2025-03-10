# Special

## Поднятие контейнера с базой данных:
#### docker run --name special -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=special -p 5436:5432 -d postgres:latest