from app.controllers.datarecord import UserRecord, MessageRecord, DataRecord
from bottle import template, redirect, request, response, Bottle, static_file
import socketio
import json

class Application:

    def __init__(self):
        self.pages = {
            'portal': self.portal,
            'pagina': self.pagina,
            'create': self.create,
            'delete': self.delete,
            'chat': self.chat,
            'edit': self.edit,
            'app': self._app
        }
        self.__users = UserRecord()
        self.__messages = MessageRecord()
        self.__current_login = None
        self.edited = None
        self.removed = None
        self.created= None
        self.__produtos = DataRecord()
        self.app = Bottle()
        self.setup_routes()
        self.sio = socketio.Server(async_mode='eventlet')
        self.setup_websocket_events()
        self.wsgi_app = socketio.WSGIApp(self.sio, self.app)

    def setup_routes(self):
        @self.app.route('/static/<filepath:path>')
        def serve_static(filepath):
            return static_file(filepath, root='./app/static')

        @self.app.route('/favicon.ico')
        def favicon():
            return static_file('favicon.ico', root='.app/static')
        
        @self.app.route('/', method='GET')
        def pagina_getter():
            return self.render('pagina')

        @self.app.route('/chat', method='GET')
        def chat_getter():
            return self.render('chat')

        @self.app.route('/portal', method='GET')
        def portal_getter():
            return template('app/views/html/page_app')

        @self.app.route('/portal', method='POST')
        def portal_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            session_id = self.__users.checkUser(username, password)
            print(f"{username}, {password}")
            if session_id:
                self.logout_user()
                response.set_cookie('session_id', session_id, httponly=True, secure=False, max_age=3600)
                print(f"cookie {session_id}")
                redirect('/main')
            else:
                print("deu erro")
                return template('app/views/html/page_app', 
                        error="Usuário ou senha inválidos",
                        username=username, 
                        removed=None, 
                        created=None, 
                        edited=None)

        @self.app.route('/main', method='GET')
        def main_page():
            current_user = self.getCurrentUserBySessionId()
            if current_user:
                tipo = getattr(current_user, 'tipo', 'comum')
                produtos_json = json.dumps(self.__produtos.getAllProducts())
                lojas_json = json.dumps(self.__produtos.getAllStores())
                return template('app/views/html/main.html',
                                user_type_raw=tipo,
                                user_type_json=json.dumps(tipo),
                                itens=produtos_json,
                                lojas=lojas_json)
            else:
                redirect('/portal')

        @self.app.route('/logout', method='POST')
        def logout_action():
            self.logout_user()
            return self.render('portal')

        @self.app.route('/app', methods=['GET'])
        @self.app.route('/app/<username>', methods=['GET'])
        def activate_page(username=None):
            if not username:
                return self.render('app')
            else:
                return self.render('app', username)
            
        @self.app.route('/solicitar-acesso', method='GET')
        def request_access_form():
            return template('app/views/html/solicitar_acesso.html', success_message=None)

        @self.app.route('/solicitar-acesso', method='POST')
        def request_access_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            self.__users.request_access(username, password)
            return template('app/views/html/solicitar_acesso.html', success_message="Sua solicitação foi enviada com sucesso!")

        @self.app.route('/admin/users', method='GET')
        def admin_users_panel():
            current_user = self.getCurrentUserBySessionId()
            if not current_user or getattr(current_user, 'tipo', 'comum') != 'adm':
                return "<h1>Acesso Negado</h1><p>Você não tem permissão para acessar esta página.</p>"
            all_users = self.__users.getUserAccounts()
            return template('app/views/html/admin_users.html', users=all_users, current_admin=current_user)

        @self.app.route('/admin/users/create', method='GET')
        def create_user_form():
            current_user = self.getCurrentUserBySessionId()
            if not current_user or getattr(current_user, 'tipo', 'comum') != 'adm':
                return "<h1>Acesso Negado</h1>"
            pending_users = self.__users.get_pending_requests()
            return template('app/views/html/create_user.html', pending_users=pending_users)

        @self.app.route('/admin/users/create', method='POST')
        def create_user_action():
            current_user = self.getCurrentUserBySessionId()
            if not current_user or getattr(current_user, 'tipo', 'comum') != 'adm':
                return "<h1>Acesso Negado</h1>"
            username = request.forms.get('username')
            password = request.forms.get('password')
            user_type = request.forms.get('user_type')
            self.__users.book(username, password, user_type) 
            redirect('/admin/users')

        @self.app.route('/admin/users/approve', method='POST')
        def approve_user_action():
            current_user = self.getCurrentUserBySessionId()
            if not current_user or getattr(current_user, 'tipo', 'comum') != 'adm':
                return "<h1>Acesso Negado</h1>"
            username = request.forms.get('username')
            password = request.forms.get('password')
            user_type = request.forms.get('user_type')
            self.__users.book(username, password, user_type)
            self.__users.remove_pending_request(username)
            redirect('/admin/users/create')

        @self.app.route('/admin/users/delete/<username_to_delete>', method='POST')
        def delete_user_action(username_to_delete):
            current_user = self.getCurrentUserBySessionId()
            if not current_user or getattr(current_user, 'tipo', 'comum') != 'adm':
                return "<h1>Acesso Negado</h1>"
            if current_user.username == username_to_delete:
                return "<h1>Ação Inválida</h1><p>Você não pode excluir a si mesmo.</p>"
            self.__users.removeUser(username_to_delete)
            redirect('/admin/users')

    # método controlador de acesso às páginas:
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.app)
        if not parameter:
            return content()
        return content(parameter)

    # métodos controladores de páginas
    def getAuthenticatedUsers(self):
        return self.__users.getAuthenticatedUsers()

    def getCurrentUserBySessionId(self):
        session_id = request.get_cookie('session_id')
        return self.__users.getCurrentUser(session_id)

    def create(self):
        return template('app/views/html/create')

    def delete(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/delete', user=current_user, accounts=user_accounts)

    def edit(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/edit', user=current_user, accounts= user_accounts)

    def portal(self):
        return template('app/views/html/page_app')

    def pagina(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return template('app/views/html/pagina', transfered=True, current_user=current_user)
        return template('app/views/html/pagina', transfered=False)
    
    def app(self, parameter=None):
        if not parameter:
            return template('app/views/html/page_app',  transfered = None, data = None)
        else: 
            print(parameter)
            info = self.__users.work_with_parameter(parameter)
            if not info:
                print("Não passou")
                redirect('/app')
            else:
                return template('app/views/html/main', transfered = True, data = info)


    def get_session_id(self):
        return request.get_cookie('session_id')
    
    def is_authenticated(self, username):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return username == current_user.username
        return False

    def authenticate_user(self, username, password):
        session_id = self.__users.checkUser(username, password)
        if session_id:
            self.logout_user()
            return session_id
        return None

    def delete_user(self):
        current_user = self.getCurrentUserBySessionId()
        self.logout_user()
        self.removed= self.__users.removeUser(current_user)
        self.update_account_list()
        print(f'Valor de retorno de self.removed: {self.removed}')
        redirect('/app')

    def insert_user(self, username, password):
        self.created= self.__users.book(username, password,[])
        self.update_account_list()
        redirect('/app')

    def update_user(self, username, password):
        self.edited = self.__users.setUser(username, password)
        redirect('/app')

    def logout_user(self):
        session_id = request.get_cookie('session_id')
        self.__users.logout(session_id)
        response.delete_cookie('session_id')
        self.update_users_list()

    def chat(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            messages = self.__messages.getUsersMessages()
            auth_users= self.__users.getAuthenticatedUsers().values()
            return template('app/views/html/chat', current_user=current_user, \
            messages=messages, auth_users=auth_users)
        redirect('/app')

    def newMessage(self, message):
        try:
            content = message
            current_user = self.getCurrentUserBySessionId()
            return self.__messages.book(current_user.username, content)
        except UnicodeEncodeError as e:
            print(f"Encoding error: {e}")
            return "An error occurred while processing the message."
        
    def _app(self, parameter=None):
        if not parameter:
            return template('app/views/html/page_app', transfered=None, data=None)
        else:
            print(parameter)
            info = self.__users.work_with_parameter(parameter)  # Aqui precisa buscar pelo NOME
            if not info:
                print("Não passou")
                redirect('/app')
            else:
                return template('app/views/html/page_app', transfered=True, data=info)



    # Websocket:
    def setup_websocket_events(self):

        @self.sio.event
        async def connect(sid, environ):
            print(f'Client connected: {sid}')
            self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        @self.sio.event
        async def disconnect(sid):
            print(f'Client disconnected: {sid}')

        # recebimento de solicitação de cliente para atualização das mensagens
        @self.sio.event
        def message(sid, data):
            objdata = self.newMessage(data)
            self.sio.emit('message', {'content': objdata.content, 'username': objdata.username})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_users_event(sid, data):
            self.sio.emit('update_users_event', {'content': data})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_account_event(sid, data):
            self.sio.emit('update_account_event', {'content': data})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários LOGAR ou DESLOGAR
    # este método vai forçar esta atualização em todos os CHATS ativos. Este
    # método é chamado sempre que a rota ''
    def update_users_list(self):
        print('Atualizando a lista de usuários conectados...')
        users = self.__users.getAuthenticatedUsers()
        users_list = [{'username': user.username} for user in users.values()]
        self.sio.emit('update_users_event', {'users': users_list})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários se removerem
    # este método vai comunicar todos os Administradores ativos.
    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = self.__users.getUserAccounts()
        users_list = [{'username': user.username} for user in users]
        self.sio.emit('update_account_event', {'accounts': users_list})
