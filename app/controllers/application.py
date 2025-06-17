from bottle import template, redirect, request
from app.controllers.db.datarecord import DataRecord

class Application():

    def __init__(self):
        self.pages = {
            "app": self.app,
            "portal": self.portal
        }

        self.__models = DataRecord()
        self.__current_login = None

    def render(self,page, parameter=None):
       content = self.pages.get(page, self.helper)
       if not parameter:
           return content()
       else:
           return content(parameter)
    
    def get_session_id(self):
        return request.get_cookie('session_id')
    
    def helper(self):
        return template('app/views/html/helper')
    
    def portal(self):
        return template('app/views/html/portal')
    
    def app(self, username=None):
        if self.is_authenticated(username):
            session_id = self.get_session_id()
            user = self.__models.getCurrentUser(session_id)
            return template('app/views/html/page_app',  current_user=user)
        else: 
            return template('app/views/html/page_app', current_user=None)
    
    def is_autheticated(self, username):
        session_id = self.get_session_id()
        current_username = self.__models.getUserName(session_id)
        return username == current_username
    
    def authenticated_user(self, username, password):
        session_id = self.__models.checkUSer(username, password)
        if session_id:
            self.logout_user()
            self.__current_username = self.__models.getUserName(session_id)
            return session_id, username
        return None
    
    def logout_user(self):
        self.__current_username = None
        session_id = self.get_session_id()
        if session_id:
            self.__models.logout(session_id)