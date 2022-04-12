# reset db
rm -rf db.sqlite3
rm -rf webapp/migrations

## populate db
python manage.py makemigrations webapp
python manage.py migrate
python manage.py loaddata db.json

# creating super user
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@gmail.com', 'admin')" | python manage.py shell

