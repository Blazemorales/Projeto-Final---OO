from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:
@app.route('/app', methods=['GET'])
@app.route('/app/<username>', methods=['GET'])
def activate_page(username=None):
    if not username:
        return ctl.render('app')
    else:
        return ctl.render('app', username)

#-----------------------------------------------------------------------------
@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httplonly = True, secure=True, max_age=3600)
if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
