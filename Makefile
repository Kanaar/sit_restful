s:
	python manage.py runserver

dbdropmigrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

dbmigrate:
	python manage.py makemigrations
	python manage.py migrate

dbdrop:
	find . -path "*/db.sqlite3" -delete

dbseed:
	python seeds.py

dbreset:
	make dbdrop
	make dbdropmigrations
	make dbmigrate
	make dbseed

dbrefresh:
	python manage.py flush
	python seeds.py

demo:
	python demo.py
