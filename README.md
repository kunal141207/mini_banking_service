# Mini banking service

A Mini banking service built in flask

## Steps to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```


## Steps to celery (background verification)

No special characters are allowed in username

```bash
source venv/bin/activate
celery -A celery_tasks worker -l info
```
