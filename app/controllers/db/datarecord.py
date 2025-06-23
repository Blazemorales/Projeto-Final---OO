from tarfile import LENGTH_PREFIX
from app.models import user_account
from app.models.user_account import UserAccount
import json
import uuid

#DataRecord para o usuário
class DataRecord():
    def __init__(self):
        self.__user_accounts = []
        self.__authenticated_users = {}
        self.read()
    
    def read(self):
        try:
            with open ("app/controllers/db/user_enabled.json", "r") as arquivo_user_json:
                user_data = json.load(arquivo_user_json)
                self.user_accounts = [UserAccount(**data) for data in user_data]
                self.limit = len(self.user_accounts) - 1
        except FileNotFoundError:
            self.user_accounts.append(UserAccount('Guest', '000000'))
            self.limit = len(self.user_accounts) - 1
    
    def book(self, username, password):
        new_user = UserAccount(username, password)
        self.__user_accounts.append(new_user)
        with open("app/controllers/db/user_enabled.json", "w") as arquivo:
            user_data = [vars(user_account) for user_account in self.user_accounts]
            json.dump(user_data, arquivo)
    
    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None
        
    def getUserName(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            return None
    
    def getUserSessionId(self, username):
        for session_id in self.__authenticated_users:
            if username == self.__authenticated_users[session_id].username:
                return session_id
        return None 
    
    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4)
                self.__authenticated_users[session_id] = user
                return session_id
        return None
    
    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]


    def work_with_parameter(self, parameter):
        for user in self.user_accounts:
            if user.username == parameter:
                return user
        return None
