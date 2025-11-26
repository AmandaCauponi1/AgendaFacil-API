from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import ler, salvar, atualizar_arquivo

blp = Blueprint("Eventos", __name__, description="Gerencia os tipos de eventos")

# 1. SCHEMA
class EventoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    descricao = fields.Str(required=True)
    responsavel = fields.Str(required=True)
    publico_previsto = fields.Int(required=True)
    tipo = fields.Str(required=True)

# 2. ROTAS
@blp.route("/events")
class EventoList(MethodView):
    
    @blp.response(200, EventoSchema(many=True))
    def get(self):
        """Lista todos os eventos"""
        return ler("events")

    @blp.arguments(EventoSchema)
    @blp.response(201, EventoSchema)
    def post(self, novo_evento):
        """Cria um novo evento"""
        eventos = ler("events")
        
        novo_id = 1
        if len(eventos) > 0:
            novo_id = int(eventos[-1]['id']) + 1
        
        novo_evento['id'] = novo_id
        salvar("events", novo_evento)
        return novo_evento

@blp.route("/events/<int:evento_id>")
class EventoDetail(MethodView):
    
    @blp.response(200, EventoSchema)
    def get(self, evento_id):
        """Detalhes de um evento"""
        eventos = ler("events")
        for ev in eventos:
            if int(ev['id']) == evento_id:
                return ev
        abort(404, message="Evento não encontrado")

    @blp.arguments(EventoSchema)
    @blp.response(200, EventoSchema)
    def put(self, dados_atualizados, evento_id):
        """Atualiza dados do evento"""
        eventos = ler("events")
        encontrado = False
        
        for i, ev in enumerate(eventos):
            if int(ev['id']) == evento_id:
                dados_atualizados['id'] = evento_id
                eventos[i] = dados_atualizados
                encontrado = True
                break
        
        if not encontrado:
            abort(404, message="Evento não encontrado")
            
        atualizar_arquivo("events", eventos)
        return dados_atualizados

    @blp.response(204)
    def delete(self, evento_id):
        """Remove evento"""
        eventos = ler("events")
        
        nova_lista = [ev for ev in eventos if int(ev['id']) != evento_id]
        
        if len(nova_lista) == len(eventos):
            abort(404, message="Evento não encontrado")
            
        atualizar_arquivo("events", nova_lista)
        return ""