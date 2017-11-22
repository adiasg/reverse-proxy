uwsgi --plugins http,python3 --http 0.0.0.0:80 --wsgi-file app.py --callable app --processes 4 --threads 2
