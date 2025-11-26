from flask import Flask
from flask_smorest import Api

from resources.user import blp as UserBlueprint
from resources.space import blp as SpaceBlueprint
from resources.availability import blp as AvailabilityBlueprint
from resources.event import blp as EventBlueprint    
from resources.reservation import blp as ReservationBlueprint 

app = Flask(__name__)

app.config["API_TITLE"] = "AgendaFácil API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Registra TODAS as rotas
api.register_blueprint(UserBlueprint)
api.register_blueprint(SpaceBlueprint)
api.register_blueprint(AvailabilityBlueprint)
api.register_blueprint(EventBlueprint)      
api.register_blueprint(ReservationBlueprint) 


if __name__ == "__main__":
    app.run(debug=True)
