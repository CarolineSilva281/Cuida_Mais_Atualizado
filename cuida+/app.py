import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
import mysql.connector
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from mysql.connector.cursor import MySQLCursorDict
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = "troque-esta-chave"  # necessário para flash()
CORS(app)

# -------------------- CONFIG BANCO --------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # ajuste sua senha
    "database": "cuidaMais"
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

# -------------------- CONFIG UPLOAD --------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------- PÁGINAS (HTML) --------------------

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()
    cur_dict = conn.cursor(dictionary=True)
    
    cur_dict.execute("SELECT id_casa, nome, endereco, telefone, vagas, descricao, imagem FROM casas ORDER BY criado_em DESC")
    casas = cur_dict.fetchall()
    
    # --- LINHA CORRIGIDA AQUI ---
    cur.execute("SELECT id_plano, nome_plano, descricao, preco FROM planos ORDER BY preco ASC")
    planos = cur.fetchall()
    
    cur.close()
    cur_dict.close()
    conn.close()
    
    return render_template("index.html", casas=casas, planos=planos)

@app.route("/planos")
def planos():
    conn = get_conn()
    cur_dict = conn.cursor(dictionary=True)
    # --- LINHA CORRIGIDA AQUI ---
    cur_dict.execute("SELECT id_plano, nome_plano, descricao, preco FROM planos ORDER BY preco ASC")
    planos_do_db = cur_dict.fetchall()
    cur_dict.close()
    conn.close()
    return render_template("planos.html", planos=planos_do_db)

@app.route("/cadastrar_casa", methods=["GET", "POST"])
def cadastrar_casa_page():
    conn = get_conn()
    cur = conn.cursor()
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        descricao = request.form.get("descricao")
        vagas = request.form.get("vagas")
        senha = request.form.get("senha")
        id_plano = request.form.get("plano")
        
        # --- TRATAMENTO DA IMAGEM ---
        imagem = request.files.get("imagem")
        nome_arquivo = "default.jpg"
        
        if imagem and imagem.filename != "":
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            
        # Criptografa a senha antes de salvar
        senha_hash = generate_password_hash(senha)
        
        cur.execute("""
            INSERT INTO casas (nome, email, telefone, endereco, descricao, vagas, senha, id_plano, imagem)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, endereco, descricao, vagas, senha_hash, id_plano, nome_arquivo))
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash("Casa cadastrada com sucesso!", "success")
        return redirect(url_for("cadastrar_casa_page"))
    else:
        # Método GET
        cur.execute("SELECT id_plano, nome_plano FROM planos ORDER BY nome_plano")
        planos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("cadastrar_casa.html", planos=planos)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id_casa, nome, senha FROM casas WHERE email = %s", (email,))
        casa = cur.fetchone()
        cur.close()
        conn.close()
        
        if casa and check_password_hash(casa[2], senha):
            session["casa_id"] = casa[0]
            session["casa_nome"] = casa[1]
            flash(f"Bem-vindo, {casa[1]}!", "success")
            return redirect(url_for("painel"))
        else:
            flash("Email ou senha incorretos.", "danger")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta com sucesso.", "info")
    return redirect(url_for("login"))

@app.route("/enviar_solicitacao", methods=["POST"])
def enviar_solicitacao():
    id_casa = request.form.get("id_casa")
    nome_idoso = request.form.get("nome_idoso")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    motivo = request.form.get("motivo")
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO solicitacoes (id_casa, nome_idoso, telefone, email, motivo)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_casa, nome_idoso, telefone, email, motivo))
    conn.commit()
    cur.close()
    conn.close()
    
    flash("Solicitação enviada com sucesso!", "success")
    return redirect(url_for("home"))

@app.route("/painel")
def painel():
    if "casa_id" not in session:
        flash("Faça login para acessar o painel.", "danger")
        return redirect(url_for("login"))
    
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.*, p.nome_plano FROM solicitacoes s
        JOIN casas c ON s.id_casa = c.id_casa
        JOIN planos p ON c.id_plano = p.id_plano
        WHERE s.id_casa = %s ORDER BY s.criado_em DESC
    """, (session["casa_id"],))
    solicitacoes = cur.fetchall()
    
    for solic in solicitacoes:
        solic['criado_em'] = solic['criado_em'].strftime('%d/%m/%Y às %H:%M')
        
    cur.close()
    conn.close()
    
    return render_template("painel.html", solicitacoes=solicitacoes)

# -------------------- API CASAS --------------------
@app.route("/api/casas", methods=["POST"])
def cadastrar_casa_api():
    dados = request.get_json(force=True)
    
    conn = get_conn()
    cur = conn.cursor()
    
    senha_hash = generate_password_hash(dados.get('senha'))
    
    cur.execute("""
        INSERT INTO casas (nome, endereco, telefone, email, senha, vagas, descricao, imagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        dados.get('nome'),
        dados.get('endereco'),
        dados.get('telefone'),
        dados.get('email'),
        senha_hash,
        dados.get('vagas', 0),
        dados.get('descricao'),
        dados.get('imagem', 'default.jpg')
    ))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"mensagem": "Casa cadastrada com sucesso!"}), 201

# -------------------- DELETAR CASA --------------------
@app.route("/deletar_casa/<int:id_casa>", methods=["POST"])
def deletar_casa(id_casa):
    if "casa_id" not in session or session["casa_id"] != id_casa:
        flash("Ação não permitida!", "danger")
        return redirect(url_for("home"))
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM casas WHERE id_casa = %s", (id_casa,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Casa excluída com sucesso!", "success")
    return redirect(url_for("home"))

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(debug=True)