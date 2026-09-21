

from flask import Flask
from app.views import register_routes
from app.database import criar_banco

app = Flask(__name__)
app.secret_key = 'chave-secreta-do-projeto'
criar_banco()
register_routes(app)
if __name__ == '__main__':
    app.run(debug=True)
    