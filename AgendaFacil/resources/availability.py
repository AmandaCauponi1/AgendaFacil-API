from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import ler, salvar

blp = Blueprint("Disponibilidade", __name__, description="Gerencia horários livres")

# 1. SCHEMA
class DisponibilidadeSchema(Schema):
    id = fields.Int(dump_only=True)
    espaco_id = fields.Int(required=True, metadata={"description": "ID do Espaço (Sala/Auditório)"})
    data = fields.Str(required=True, metadata={"description": "Formato: YYYY-MM-DD"})
    turno = fields.Str(required=True, metadata={"description": "manhã, tarde ou noite"})

class FiltroDataSchema(Schema):
    date = fields.Str(required=False, metadata={"description": "Filtrar por data (YYYY-MM-DD)"})

# 2. ROTAS
@blp.route("/availability")
class DisponibilidadeList(MethodView):
    
    @blp.arguments(FiltroDataSchema, location="query") 
    @blp.response(200, DisponibilidadeSchema(many=True))
    def get(self, args):
        """Lista horários disponíveis (Opcional: filtrar por data)"""
        todos = ler("availabilities")
        
        data_filtro = args.get("date")
        if data_filtro:
            resultado = [d for d in todos if d['data'] == data_filtro]
            return resultado
        
        return todos

    @blp.arguments(DisponibilidadeSchema)
    @blp.response(201, DisponibilidadeSchema)
    def post(self, nova_disp):
        """Cadastra um novo horário disponível"""
        todos = ler("availabilities")
        
        novo_id = 1
        if len(todos) > 0:
            novo_id = int(todos[-1]['id']) + 1
        
        nova_disp['id'] = novo_id
        

        salvar("availabilities", nova_disp)
        return nova_disp