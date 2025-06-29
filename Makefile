run:
	python manage.py runserver 9000

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

collectstatic:
	python manage.py collectstatic --noinput

test:
	python manage.py test

redis:
	redis-server

celery:
	celery -A ipinfo_project worker --loglevel=info


superuser:
	python manage.py createsuperuser

daphne:
	python -m daphne -p 8000 ipinfo_project.asgi:application   

workers:
	celery -A ipinfo_project worker --concurrency=4 --loglevel=info --pool=threads

wstest:
	pytest ipcheck/tests/test_ws.py