python manage.py makemigrations
python manage.py migrate
touch /log.log
cp conf/nginx.conf /etc/nginx/sites-enabled/default
service nginx start
uwsgi --socket :9001 --module adminPanel.wsgi
tail -f /log.log