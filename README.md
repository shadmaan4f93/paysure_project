Basic implementation of insurer project


clone repository from : https://github.com/shadmaan4f93/paysure_project.git

 pip install -r requirements.txt

    python manage.py makemigrations
    python manage.py migrate

    python manage.py makemigrations insurer
    python manage.py migrate


    Python manage.py runserver


 Endpoints are exposed as

 uploading policy : http://127.0.0.1:8000/policy/
 authorizing payments : http://127.0.0.1:8000/payment/