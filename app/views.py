from flask import app, render_template, request, redirect, url_for

import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash


def register_routes(app):

    # Rota da página inicial
    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    # Rota login
    @app.route('/login', methods=["GET", "POST"])
    def login():

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            # Conecta ao banco
            conexao = sqlite3.connect("database.db")
            cursor = conexao.cursor()

            # Consulta o usuário no banco
            cursor.execute(
                "SELECT * FROM usuarios WHERE username = ?",
                (username,)
            )

            usuario = cursor.fetchone()
            conexao.close()

            # Verifica se o usuário existe e se a senha está correta
            if usuario:
                if check_password_hash(usuario[2], password):
                    return render_template('user.html', username=username)
                else:
                    return render_template(
                        'login.html',
                        error="Usuário ou senha incorretos."
                    )
            else:
                return render_template(
                    'login.html',
                    error="Usuário ou senha incorretos."
                )

        # Quando a página é acessada pelo navegador (GET)
        return render_template(
            'login.html',
            success=request.args.get("registered")
        )

    # Rota do perfil
    @app.route('/usuarios', methods=["GET", "POST"])
    def usuarios():
        return render_template(
            'user.html',
            username=request.form.get("username")
        )

    # Rota de registro
    @app.route('/registrar', methods=["GET", "POST"])
    def registrar():

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            senha_hash = generate_password_hash(password)

            conexao = sqlite3.connect("database.db")
            cursor = conexao.cursor()

            try:
                cursor.execute(
                    "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                    (username, senha_hash)
                )
            except sqlite3.IntegrityError:
                conexao.close()
                return render_template(
                    'registrar.html',
                    error="Nome de usuário já está em uso."
                )

            conexao.commit()
            conexao.close()

            print("Usuário cadastrado:", username)
            print("Senha recebida")
            return redirect(url_for('login', registered='1'))

        return render_template('registrar.html')
