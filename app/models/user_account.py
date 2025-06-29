class UserAccount():
    
    def __init__(self, username, password, tipo='comum'):
        self.username = username
        self.password = password
        self.tipo = tipo  # ← Agora UserAccount tem o atributo 'tipo'

    def isAdmin(self):
        return False


class SuperAccount(UserAccount):
    
    def __init__(self, username, password, permissions, tipo='adm'):
        super().__init__(username, password, tipo)
        self.permissions = permissions if permissions else ['user']

    def isAdmin(self):
        return True
