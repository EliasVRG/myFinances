import json
from flask import Flask, send_file, redirect, url_for, request, make_response, render_template
import os
import datetime
from collections import defaultdict


print("\nLendo arquivo de configuração de ambiente...")

# Local
prefix = ''

# Dicionário para mapear tokens de sessão a nomes de usuário
sessions = {}

def prepare_chart_data(transactions):
    # Inicializa os dicionários para armazenar os dados do gráfico
    monthly_expenses = defaultdict(float)
    expense_distribution = defaultdict(float)
    category_comparison = defaultdict(float)

    # Cria uma lista de meses vazios para garantir que todos os meses estejam presentes
    monthly_expenses_data = [0] * 12

    # Processa cada transação
    for transaction in transactions:
        date = datetime.datetime.strptime(transaction['date'], '%Y-%m-%d')
        month_year = date.strftime('%Y-%m')
        month = date.month

        value = transaction['value']
        category = transaction['category']

        # Agrupa os gastos mensais
        if transaction['type'] == 'saida':
            monthly_expenses[month_year] += value
            monthly_expenses_data[month - 1] += abs(value)  # Adiciona o valor absoluto

        # Agrupa a distribuição de saídas por categoria
        if transaction['type'] == 'saida':
            expense_distribution[category] += value

        # Comparação por categoria
        category_comparison[category] += value
    
    # Prepara os dados no formato necessário para o Chart.js
    chart_data = {
        'financialOverview': {
            'labels': list(monthly_expenses.keys()),
            'data': list(monthly_expenses.values())
        },
        'monthlyExpenses': {
            'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            'data': monthly_expenses_data
        },
        'expenseDistribution': {
            'labels': list(expense_distribution.keys()),
            'data': list(expense_distribution.values())
        },
        'categoryComparison': {
            'labels': list(category_comparison.keys()),
            'data': list(category_comparison.values())
        }
    }

    return chart_data


# Função para calcular entradas, saídas e saldo atual do dia
def calculate_today_transactions(username):
    transactions = load_transactions()
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    today_entries = 0.0
    today_exits = 0.0
    
    # Calcula entradas e saídas do dia atual
    for t in transactions:
        if t['user'] == username and t['date'] == today:
            if t['type'] == 'entrada':
                today_entries += float(t['value'])
            elif t['type'] == 'saida':
                today_exits += float(t['value'])
    
    # Calcula o saldo atual
    current_balance = 0.0
    for t in transactions:
        if t['user'] == username:
            if t['type'] == 'entrada':
                current_balance += float(t['value'])
            elif t['type'] == 'saida':
                current_balance += float(t['value'])
    
    return today_entries, today_exits, current_balance

# Função auxiliar para adicionar o prefixo '/api'
def prefixed_url_for(endpoint, **values):
    url = url_for(endpoint, **values)
    if url.startswith('/'):
        url = prefix + url
    return url

# Função auxiliar para verificar a autenticação
def is_authenticated():
    session_token = request.cookies.get('session_token')
    app.logger.info(f"Token de sessão: {session_token}")
    if session_token and session_token in sessions:
        username = sessions[session_token]['username']
        app.logger.info(f"Usuário encontrado na sessão: {username}")
        return True
    else:
        app.logger.info("Token de sessão não encontrado ou inválido.")
        return False

# Função auxiliar para obter o nível de acesso do usuário
def get_user_access():
    session_token = request.cookies.get('session_token')
    if session_token and session_token in sessions:
        app.logger.info(f"Nível de acesso do usuário: {sessions[session_token]['access']}")
        return sessions[session_token]['access']
    return None

# Função para ler usuários do arquivo JSON
def load_users():
    try:
        # Caminho absoluto para o arquivo users.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'users.json')
        
        with open(file_path, 'r') as f:
            app.logger.info("Lendo 'users.json'...")
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo 'users.json' não encontrado no caminho: {file_path}")
        return {}

# Função para salvar usuários no arquivo JSON
def save_users(users):
    try:
        # Caminho absoluto para o arquivo users.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'users.json')
        
        with open(file_path, 'w') as f:
            app.logger.info("Salvando 'users.json'...")
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar 'users.json': {e}")

# Função para obter as últimas 5 transações de um usuário
def get_last_5_transactions(username):
    transactions = load_transactions()
    user_transactions = [t for t in transactions if t['user'] == username]
    return user_transactions[-5:]

# Função para obter as transações de um usuário
def get_transactions(username):
    transactions = load_transactions()
    user_transactions = [t for t in transactions if t['user'] == username]
    return user_transactions

# Função para ler transações do arquivo JSON
def load_transactions():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, './extrato/transactions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Função para salvar transações no arquivo JSON
def save_transactions(transactions):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, './extrato/transactions.json')
        with open(file_path, 'w') as f:
            json.dump(transactions, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar 'transactions.json': {e}")

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False  # Configuração para lidar com caracteres não-ASCII

@app.route('/transactions', methods=['GET'])
def transactions():
    if not is_authenticated():
        app.logger.info("Usuário não autenticado. Redirecionando para a página de login.")
        return redirect(prefixed_url_for('authentication'))
    else:
        session_token = request.cookies.get('session_token')
        username = sessions[session_token]['username']
        users = load_users()
        if username in users:
            last_5_transactions = get_last_5_transactions(username)
            today_entries, today_exits, current_balance = calculate_today_transactions(username)
            return render_template('index.html', transactions=last_5_transactions, today_entries=today_entries, today_exits=today_exits, current_balance=current_balance)
        else:
            return render_template('login.html', info='Permissões inválidas. Por favor, faça login novamente.')

@app.route('/extract', methods=['GET'])
def extract():
    if not is_authenticated():
        app.logger.info("Usuário não autenticado. Redirecionando para a página de login.")
        return redirect(prefixed_url_for('authentication'))
    else:
        session_token = request.cookies.get('session_token')
        username = sessions[session_token]['username']
        transactions = get_transactions(username)
        return render_template('extract.html', transactions=transactions)

@app.route('/authentication', methods=['GET', 'POST'])
def authentication():
    print("Chamada para a rota '/authentication'")

    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            print("Campos 'username' ou 'password' não presentes no formulário.")
            return render_template('login.html', info='Campos obrigatórios não preenchidos.')

        username = request.form['username']
        password = request.form['password']
        print("Tentativa de login para o usuário:", username)
        
        users = load_users()
        # Verifica as credenciais
        if username in users and users[username]['password'] == password:
            # Gera um token de sessão e redireciona para a página de transações
            session_token = username + '_session_token'
            sessions[session_token] = {
                'username': username,
                'access': users[username].get('access', 'user')  # Usar 'user' como valor padrão
            }
            resp = make_response(redirect(prefixed_url_for('transactions')))
            resp.set_cookie('session_token', session_token)
            return resp
        else:
            print("Usuário ou senha inválidos")
            return render_template('login.html', info='Usuário ou senha inválidos')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session_token = request.cookies.get('session_token')
    if session_token in sessions:
        sessions.pop(session_token)
    resp = make_response(redirect(prefixed_url_for('authentication')))
    resp.set_cookie('session_token', '', expires=0)  # Remove o cookie de sessão
    return resp

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        app.logger.info("Requisição GET recebida para '/cadastro'. Renderizando cadastro.html.")
        return render_template('cadastro.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        app.logger.info(f"Requisição POST recebida para '/cadastro' com dados: username={username}, password={password}.")
        
        users = load_users()
        
        if username not in users:
            users[username] = {
                'password': password,
                'access': 'user'
            }
            save_users(users)
            app.logger.info(f"Usuário '{username}' registrado com sucesso. Redirecionando para a página de login.")
            return redirect(prefixed_url_for('authentication'))
        else:
            app.logger.info(f"Cadastro falhou. O usuário '{username}' já existe.")
            return render_template('cadastro.html', info='Usuário já existe')
    
    app.logger.error("Método de requisição inválido recebido para '/cadastro'. Redirecionando para a página de cadastro.")
    return redirect(prefixed_url_for('cadastro'))

# Rota para adicionar transação
@app.route('/addTransaction', methods=['POST'])
def add_transaction():
    if not is_authenticated():
        return redirect(prefixed_url_for('authentication'))
    
    value = float(request.form['value'])
    if request.form['type'] == 'saida':
        value = -abs(value)  # Garantir que o valor seja negativo
    
    transaction = {
        'user': sessions[request.cookies.get('session_token')]['username'],
        'date': request.form['date'],
        'type': request.form['type'],
        'description': request.form['description'],
        'category': request.form['category'],
        'value': value
    }
    
    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)
    
    return redirect(prefixed_url_for('transactions'))

# Rota para exibir relatórios em formato JSON
@app.route('/reports', methods=['GET'])
def reports():
    # Verifica se o usuário está autenticado (por exemplo, verificando a sessão)
    if not is_authenticated():
        app.logger.info("Usuário não autenticado. Redirecionando para a página de login.")
        return redirect(prefixed_url_for('authentication'))
    else:
        session_token = request.cookies.get('session_token')
        username = sessions[session_token]['username']
        
        # Aqui você precisa obter as transações do usuário com o username fornecido
        transactions = get_transactions(username)
        
        # Prepara os dados para serem exibidos no gráfico
        chart_data = prepare_chart_data(transactions)

        print(chart_data)
        
        # Retorna os dados em formato JSON para o gráfico
        return render_template('reports.html', chart_data=chart_data)
    

# Configuração para permitir acesso ao cookie de sessão pelo JavaScript
app.config['SESSION_COOKIE_HTTPONLY'] = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8067, debug=True)
