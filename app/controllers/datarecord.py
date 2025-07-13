from app.models.user_account import UserAccount, SuperAccount
from app.models.user_message import UserMessage
from app.models.product import Product
from app.models.store import Store
import json
import uuid


class MessageRecord():
    """Banco de dados JSON para o recurso: Mensagem"""

    def __init__(self):
        self.__user_messages= []
        self.read()


    def read(self):
        try:
            with open("app/controllers/db/user_messages.json", "r") as fjson:
                user_msg = json.load(fjson)
                self.__user_messages = [UserMessage(**msg) for msg in user_msg]
        except FileNotFoundError:
            print('Não existem mensagens registradas!')


    def __write(self):
        try:
            with open("app/controllers/db/user_messages.json", "w") as fjson:
                user_msg = [vars(user_msg) for user_msg in \
                self.__user_messages]
                json.dump(user_msg, fjson)
                print(f'Arquivo gravado com sucesso (Mensagem)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Mensagem)!')


    def book(self,username,content):
        new_msg= UserMessage(username,content)
        self.__user_messages.append(new_msg)
        self.__write()
        return new_msg


    def getUsersMessages(self):
        return self.__user_messages


# ------------------------------------------------------------------------------

class UserRecord():
    """Banco de dados JSON para o recurso: Usuário"""

    def __init__(self):
        self.__allusers= {'user_accounts': [], 'super_accounts': []}
        self.__authenticated_users = {}
        self.read('user_accounts')
        self.read('super_accounts')


    def read(self,database):
        account_class = SuperAccount if (database == 'super_accounts' ) else UserAccount
        try:
            with open(f"app/controllers/db/{database}.json", "r") as fjson:
                user_d = json.load(fjson)
                self.__allusers[database]= [account_class(**data) for data in user_d]
        except FileNotFoundError:
            self.__allusers[database].append(account_class('Guest', '000000'))


    def __write(self,database):
        try:
            with open(f"app/controllers/db/{database}.json", "w") as fjson:
                user_data = [vars(user_account) for user_account in \
                self.__allusers[database]]
                json.dump(user_data, fjson)
                print(f'Arquivo gravado com sucesso (Usuário)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Usuário)!')



    def setUser(self,username,password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if username == user.username:
                    user.password= password
                    print(f'O usuário {username} foi editado com sucesso.')
                    self.__write(account_type)
                    return username
        print('O método setUser foi chamado, porém sem sucesso.')
        return None


    def get_pending_requests(self):
        """Lê e retorna a lista de solicitações pendentes."""
        try:
            with open("app/controllers/db/pending_users.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] # Retorna lista vazia se o arquivo não existe ou está vazio

    def request_access(self, username, password):
        """Salva uma nova solicitação de acesso."""
        pending_list = self.get_pending_requests()
        pending_list.append({'username': username, 'password': password})
        with open("app/controllers/db/pending_users.json", "w") as f:
            json.dump(pending_list, f, indent=4)
        print(f"Nova solicitação de acesso para '{username}' foi salva.")

    def remove_pending_request(self, username):
        """Remove uma solicitação da lista de pendentes após ser aprovada."""
        pending_list = self.get_pending_requests()
        # Cria uma nova lista sem o usuário que foi aprovado
        updated_list = [req for req in pending_list if req['username'] != username]
        with open("app/controllers/db/pending_users.json", "w") as f:
            json.dump(updated_list, f, indent=4)
        print(f"Solicitação de '{username}' foi removida da lista de pendentes.")

    def removeUser(self, username_to_delete):  # O parâmetro agora é o NOME do usuário (uma string)
        for account_type in ['user_accounts', 'super_accounts']:
            
            user_object_to_remove = None
            # Procura o OBJETO do usuário na lista correspondente
            for user in self.__allusers[account_type]:
                if user.username == username_to_delete:
                    user_object_to_remove = user
                    break  # Encontrou o usuário, pode parar de procurar nesta lista

            if user_object_to_remove:
                print(f'O usuário "{username_to_delete}" foi encontrado no cadastro de {account_type}.')
                
                # Remove o OBJETO da lista
                self.__allusers[account_type].remove(user_object_to_remove)
                
                self.__write(account_type)
                
                print(f'Usuário "{username_to_delete}" foi removido com sucesso.')
                return username_to_delete  # Retorna o nome do usuário que foi removido
                
        print(f'O usuário "{username_to_delete}" não foi identificado em nenhum cadastro!')
        return None


# Em app/controllers/datarecord.py
# Substitua seu método book por este:

    def book(self, username, password, tipo):
        if tipo == "adm":
            # CORREÇÃO: Adicionamos o argumento 'permissions' que estava faltando.
            # Por enquanto, passaremos uma lista vazia [].
            new_user = SuperAccount(username, password, permissions=[])
            self.__allusers['super_accounts'].append(new_user)
            self.__write('super_accounts')
        else:
            new_user = UserAccount(username, password)
            self.__allusers['user_accounts'].append(new_user)
            self.__write('user_accounts')
        
        # MELHORIA: Garante que o atributo 'tipo' seja definido no objeto,
        # caso o construtor da classe não faça isso automaticamente.
        if not hasattr(new_user, 'tipo'):
            new_user.tipo = tipo
        
        print(f"Usuário '{username}' do tipo '{tipo}' criado com sucesso.")
        return new_user.username


    # Em datarecord.py
    def getUserAccounts(self):
        return self.__allusers['user_accounts'] + self.__allusers['super_accounts']

    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getAuthenticatedUsers(self):
        return self.__authenticated_users


    def checkUser(self, username, password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username and user.password == password:
                    session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                    self.__authenticated_users[session_id] = user
                    return session_id  # Retorna o ID de sessão para o usuário
        return None
    
    def work_with_parameter(self, username):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username:
                    return user
        return None



    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado

class DataRecord:
    """Gerencia produtos e lojas a partir de arquivos JSON"""

    def __init__(self):
        self.__products = []
        self.__stores = []
        self.read_products()
        self.read_stores()

    def read_products(self):
        try:
            with open("app/controllers/db/products.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.__products = [Product(**item) for item in data]
        except FileNotFoundError:
            print("Arquivo products.json não encontrado.")
            self.__products = []

    def read_stores(self):
        try:
            with open("app/controllers/db/stores.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.__stores = [Store(**item) for item in data]
        except FileNotFoundError:
            print("Arquivo stores.json não encontrado.")
            self.__stores = []

    def getAllProducts(self):
        # Retorna lista de dicts para facilitar uso no template
        return [vars(prod) for prod in self.__products]

    def getAllStores(self):
        return [vars(store) for store in self.__stores]


    def __write_products(self):
        """Salva a lista de produtos atual no arquivo JSON."""
        try:
            with open("app/controllers/db/products.json", "w", encoding="utf-8") as f:
                # Converte a lista de objetos Product em uma lista de dicionários
                list_of_dicts = [vars(prod) for prod in self.__products]
                json.dump(list_of_dicts, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar produtos: {e}")

    def __write_stores(self):
        """Salva a lista de lojas atual no arquivo JSON."""
        try:
            with open("app/controllers/db/stores.json", "w", encoding="utf-8") as f:
                list_of_dicts = [vars(store) for store in self.__stores]
                json.dump(list_of_dicts, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar lojas: {e}")
            
# Em app/controllers/datarecord.py, dentro da classe DataRecord

    def add_store(self, nome, endereco, telefone):
        """Adiciona uma nova loja e salva no JSON."""
        new_id = str(uuid.uuid4()) # Gera um ID único
        new_store = Store(id=new_id, nome=nome, endereco=endereco, telefone=telefone)
        self.__stores.append(new_store)
        self.__write_stores()
        return new_store

    def add_product(self, nome, descricao, preco, estoque, loja_id):
        """Adiciona um novo produto e salva no JSON."""
        new_id = str(uuid.uuid4())
        # Tenta converter preco para float e estoque para int
        try:
            preco = float(preco)
            estoque = int(estoque)
        except (ValueError, TypeError):
            print("Erro: Preço ou estoque inválido.")
            return None
        
        new_prod = Product(id=new_id, nome=nome, descricao=descricao, preco=preco, estoque=estoque)
        # O modelo de produto que você mandou não tem loja_id, mas é uma boa prática ter.
        # Se quiser associar, adicione `loja_id` ao __init__ da classe Product.
        # Por agora, não vamos associar.
        self.__products.append(new_prod)
        self.__write_products()
        return new_prod

    def update_product_stock(self, product_id, new_stock):
        """Atualiza o estoque de um produto específico."""
        for product in self.__products:
            if product.id == product_id:
                try:
                    product.estoque = int(new_stock)
                    self.__write_products()
                    return product
                except (ValueError, TypeError):
                    return None
        return None

    def delete_product(self, product_id):
        """Exclui um produto da lista."""
        product_found = any(p.id == product_id for p in self.__products)
        if product_found:
            self.__products = [p for p in self.__products if p.id != product_id]
            self.__write_products()
            return True
        return False
    
# Em app/controllers/datarecord.py, dentro da classe DataRecord

# Substitua sua função delete_store por esta versão com prints

    def delete_store(self, store_id):
        """Exclui uma loja da lista com base no seu ID."""
        
        # --- DEBUG Prints ---
        print("-" * 40)
        print(f"Tentando excluir ID recebido: '{store_id}' (Tipo: {type(store_id)})")
        
        # Vamos imprimir todos os IDs que temos na memória para comparar
        ids_na_memoria = [s.id for s in self.__stores]
        print(f"IDs de lojas atualmente na memória: {ids_na_memoria}")
        # --------------------

        store_to_delete = None
        for store in self.__stores:
            # --- DEBUG Print dentro do loop ---
            print(f"Comparando '{store_id}' com '{store.id}' (Tipo: {type(store.id)})")
            # --------------------------------

            # Comparando os valores como strings para garantir a correspondência
            if str(store.id) == str(store_id):
                store_to_delete = store
                print(f"LOJA ENCONTRADA: {store.nome}")
                break # Encontrou a loja, pode parar o loop

        if store_to_delete:
            self.__stores.remove(store_to_delete)
            self.__write_stores() # Tenta salvar no arquivo
            print(f"Loja com ID {store_id} foi REMOVIDA da lista em memória e salva.")
            print("-" * 40)
            return True
        
        print(f"Tentativa de excluir loja com ID {store_id}, mas NÃO FOI ENCONTRADA na lista.")
        print("-" * 40)
        return False