from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import ler, salvar, atualizar_arquivo # <--- Importamos a nova função

blp = Blueprint("Espacos", __name__, description="Gerenciamento de Salas e Auditórios")

# 1. SCHEMA
class EspacoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, metadata={"description": "Ex: Sala 101"})
    bloco = fields.Str(required=True, metadata={"description": "Ex: Bloco A"})
    capacidade = fields.Int(required=True)

# 2. ROTAS DE LISTAGEM E CRIAÇÃO
@blp.route("/spaces")
class EspacoList(MethodView):
    
    @blp.response(200, EspacoSchema(many=True))
    def get(self):
        """Lista todos os espaços"""
        return ler("spaces")

    @blp.arguments(EspacoSchema)
    @blp.response(201, EspacoSchema)
    def post(self, novo_espaco):
        """Cadastra novo espaço"""
        espacos = ler("spaces")
        
        novo_id = 1
        if len(espacos) > 0:
            novo_id = int(espacos[-1]['id']) + 1
        
        novo_espaco['id'] = novo_id
        salvar("spaces", novo_espaco)
        return novo_espaco

# 3. ROTAS ESPECÍFICAS (GET, PUT, DELETE por ID)
@blp.route("/spaces/<int:espaco_id>")
class EspacoDetail(MethodView):
    
    @blp.response(200, EspacoSchema)
    def get(self, espaco_id):
        """Retorna detalhes de um espaço"""
        espacos = ler("spaces")
        for espaco in espacos:
            if int(espaco['id']) == espaco_id:
                return espaco
        abort(404, message="Espaço não encontrado")

    @blp.arguments(EspacoSchema)
    @blp.response(200, EspacoSchema)
    def put(self, dados_atualizados, espaco_id):
        """Atualiza um espaço existente"""
        espacos = ler("spaces")
        espaco_encontrado = False
        
        for i, espaco in enumerate(espacos):
            if int(espaco['id']) == espaco_id:

                dados_atualizados['id'] = espaco_id
                espacos[i] = dados_atualizados
                espaco_encontrado = True
                break
        
        if not espaco_encontrado:
            abort(404, message="Espaço não encontrado")
            
        atualizar_arquivo("spaces", espacos)
        
        return dados_atualizados

    @blp.response(204)
    def delete(self, espaco_id):
        """Remove um espaço"""
        espacos = ler("spaces")
        espaco_encontrado = False
        
        nova_lista = [e for e in espacos if int(e['id']) != espaco_id]
        
        if len(nova_lista) == len(espacos):
             abort(404, message="Espaço não encontrado")
        
        atualizar_arquivo("spaces", nova_lista)
        return ""