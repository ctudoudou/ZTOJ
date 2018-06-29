此文件夹下的代码将运行于服务器中，代码为网站运行代码

启动命令
```shell
redis-server
python manage.py runserver
celery -A web worker -l info
```