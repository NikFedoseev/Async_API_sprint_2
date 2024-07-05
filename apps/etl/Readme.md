Перед запуском убедиться что есть подгоовленная БД со схемой content и накатанными миграциями
Далее просто выполинить команду python main.py

Загрузить дамп бд
cat dump.sql | docker exec -i your-db-container psql -U app -d movies_database