from app import celery, db
from app.models import User

import re

@celery.task
def user_verification(username):
    # some long running task here
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(string) == None):
        User.query.filter_by(username=username).update(dict(is_verified=1))
    else:
        User.query.filter_by(username=username).update(dict(is_verified=-1))
   
    db.session.commit()    
    return 1