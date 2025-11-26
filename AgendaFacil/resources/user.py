from flask.views import MethodView 
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import ler, salvar, atualizar_arquivo 

blp = Blueprint("Usuarios", __name__, description="Autenticação e Gerenciamento de Usuários")

# --- SCHEMAS ---

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    email = fields.Str(required=True)
    senha = fields.Str(required=True) 

class LoginSchema(Schema):
    email = fields.Str(required=True)
    senha = fields.Str(required=True)

class UsuarioUpdateSchema(Schema):
    nome = fields.Str()
    email = fields.Str()
    senha = fields.Str()

# --- ROTAS ---

@blp.route("/users/register")
class UsuarioRegister(MethodView):
    @blp.arguments(UsuarioSchema)
    @blp.response(201, UsuarioSchema)
    def post(self, dados_novos):
        """Cadastra novo usuário"""
        usuarios = ler("users")
        for u in usuarios:
            if u['email'] == dados_novos['email']:
                abort(409, message="Email já cadastrado.")
        novo_id = 1
        if len(usuarios) > 0:
            novo_id = int(usuarios[-1]['id']) + 1

        dados_novos['id'] = novo_id
        salvar("users", dados_novos)
        return dados_novos

@blp.route("/users/login")
class UsuarioLogin(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(200, description="Login realizado")
    def post(self, dados_login):
        """Realiza login"""
        usuarios = ler("users")
        for u in usuarios:
            if u['email'] == dados_login['email'] and u['senha'] == dados_login['senha']:
                return {"message": "Login realizado!", "id": u['id'], "nome": u['nome']}
        abort(401, message="Email ou senha inválidos")
        
@blp.route("/users")
class UsuarioList(MethodView):
    @blp.response(200, UsuarioSchema(many=True))
    def get(self):
        """Lista todos os usuários"""
        return ler("users")


@blp.route("/users/<int:user_id>")

class UsuarioDetail(MethodView):

    @blp.arguments(UsuarioUpdateSchema)
    @blp.response(200, UsuarioSchema)
    def put(self, dados_atualizacao, user_id):
        """Atualiza dados do usuário (Nome, Email ou Senha)"""
        usuarios = ler("users")
        usuario_encontrado = None
        indice = -1

        for i, u in enumerate(usuarios):
            if int(u['id']) == user_id:
                usuario_encontrado = u
                indice = i
                break
        
        if not usuario_encontrado:
            abort(404, message="Usuário não encontrado")

        usuario_encontrado.update(dados_atualizacao)
        
        usuarios[indice] = usuario_encontrado

        atualizar_arquivo("users", usuarios)

        return usuario_encontrado

    @blp.response(204)
    def delete(self, user_id):
        """Remove (Deleta) um usuário"""
        usuarios = ler("users")
        
        nova_lista = [u for u in usuarios if int(u['id']) != user_id]
        
        if len(nova_lista) == len(usuarios):
            abort(404, message="Usuário não encontrado")
            
        atualizar_arquivo("users", nova_lista)
        
        return ""
