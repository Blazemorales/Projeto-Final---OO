from tarfile import LENGTH_PREFIX
from app.models import user_account
from app.models.user_account import UserAccount
import json
#DataRecord para o usuário
class DataRecord():
    def __init__(self):
        self.user_accounts = []
        try:
            print("ta rodando essa bagaça?")
            with open ("app/controllers/db/user_enabled.json", "r") as arquivo_user_json:
                user_data = json.load(arquivo_user_json)
                self.user_accounts = [UserAccount(**data) for data in user_data]
                print(f"Quantidade de usuários: {len(self.user_accounts)}")
                self.limit = len(self.user_accounts) - 1
        except FileNotFoundError:
            self.user_accounts.append(UserAccount('Guest', '000000'))
            self.limit = len(self.user_accounts) - 1
    def work_with_parameter(self, parameter):
        for user in self.user_accounts:
            if user.username == parameter:
                return user
        return None
