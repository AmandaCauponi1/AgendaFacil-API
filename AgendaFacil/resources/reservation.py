from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from db import ler, salvar

blp = Blueprint("Agendamentos", __name__, description="Gerencia as reservas de salas")

# 1. SCHEMA
class ReservaSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario_id = fields.Int(required=True)
    espaco_id = fields.Int(required=True)
    evento_id = fields.Int(required=True)
    data = fields.Str(required=True, metadata={"description": "YYYY-MM-DD"})
    turno = fields.Str(required=True, metadata={"description": "manhã, tarde ou noite"})
    status = fields.Str(dump_only=True) 

# 2. ROTAS
@blp.route("/reservations")
class ReservaList(MethodView):
    
    @blp.response(200, ReservaSchema(many=True))
    def get(self):
        """Lista todas as reservas"""
        return ler("reservations")

    @blp.arguments(ReservaSchema)
    @blp.response(201, ReservaSchema)
    def post(self, nova_reserva):
        """Cria uma nova reserva"""
        reservas = ler("reservations")

        for r in reservas:
            if (r['espaco_id'] == str(nova_reserva['espaco_id']) and 
                r['data'] == nova_reserva['data'] and 
                r['turno'] == nova_reserva['turno'] and
                r['status'] != 'cancelado'):
                abort(409, message="Este espaço já está reservado neste horário!")

        novo_id = 1
        if len(reservas) > 0:
            novo_id = int(reservas[-1]['id']) + 1
        
        nova_reserva['id'] = novo_id
        nova_reserva['status'] = 'confirmado' 
        
        salvar("reservations", nova_reserva)
        return nova_reserva

# Rota Especial para Cancelar (Requisito do Professor)
@blp.route("/reservations/<int:id>/cancel")
class ReservaCancel(MethodView):
    
    @blp.response(200, description="Reserva cancelada com sucesso")
    def put(self, id):
        """Cancela uma reserva"""
        
        reservas = ler("reservations")
        reserva_alvo = None
        
        for r in reservas:
            if int(r['id']) == id:
                reserva_alvo = r.copy() 
        
        if not reserva_alvo:
            abort(404, message="Reserva não encontrada")
            
        reserva_alvo['status'] = 'cancelado'
        salvar("reservations", reserva_alvo)
        
        return {"message": "Reserva cancelada"}