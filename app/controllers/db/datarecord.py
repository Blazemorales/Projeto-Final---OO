from app.models.user_account import UserAccount
import json
#DataRecord para o usuário
class DataRecord():
    def __init__(self):
        self.user_accounts = []
        try:
            with open ("app/controllers/db/user_accounts.json", "r") as arquivo_user_json:
                user_data = json.load(arquivo_user_json)
                self.user_accounts = [UserAccount(**data) for data in user_data]
                self.limit = len(self.user_accounts) - 1
        except FileNotFoundError:
            self.user_accounts.append(UserAccount('Guest', '000000'))
            self.limit = len(self.user_accounts) - 1
    def work_with_parameter(self, parameter):
        try:
            index = int(parameter)
            if index <= self.limit:
                return self.user_accounts[index]
        except (ValueError, IndexError):
            return None