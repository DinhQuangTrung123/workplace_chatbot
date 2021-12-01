#!/bin/sh
PYTHON_ENV=/app/workplace_chatbot/django-venv-chatbot/bin/python3.6
PYTHON_SERVER='app.py'


stop_app(){
        kill -9 `ps -ef | grep $PYTHON_ENV  | grep -v grep | awk '{print $2}'`
}

start_app() {
        nohup $PYTHON_ENV manage.py runserver 0.0.0.0:8000 &
}


case "$1" in
    start)
        echo "Start App"
        start_app
        ;;
    stop)
        echo "Stop App"
        stop_app
        ;;
    restart)
        echo "Restart App"
        stop_app
        start_app
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 1
esac