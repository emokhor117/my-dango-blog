release: cd myBlog && python manage.py migrate --noinput
web: gunicorn myBlog.wsgi --chdir myBlog
