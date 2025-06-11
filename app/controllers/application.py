from bottle import template
from app.controllers.db.datarecord import DataRecord

class Application():

    def __init__(self):
        self.pages = {
            "app": self.app
        }

        self.models = DataRecord()

    def render(self,page, parameter=None):
       content = self.pages.get(page, self.helper)
       if not parameter:
           return content()
       else:
           return content(parameter)


    def helper(self):
        return template('app/views/html/helper')
    
    def app(self, parameter=None):
        if not parameter:
            return template('app/views/html/page_app')
        else: 
            info = self.models.work_with_parameter(parameter)
            if not info:
                redirect('/app')
            else:
                return template('app/views/html/page_app', transfered = True, data = info)
