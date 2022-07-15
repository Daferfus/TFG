from flask import current_app as app

#########
## GET ##
#########
@app.route('/hello')
def hello():
    return 'Hello, World!'