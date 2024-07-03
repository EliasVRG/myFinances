# MyFinances

## Visão Geral

MyFinances é uma aplicação web projetada para ajudar os usuários a gerenciar suas transações financeiras. O backend é construído usando Flask, um framework web WSGI leve em Python. Esta aplicação permite que os usuários façam autenticação, gerenciem transações e gerem relatórios financeiros.

# MyFinances Frontend

## Login e Registro

Para acessar a aplicação e nescessário autenticar-se ou registrar-se caso não tenha uma conta.

A tela para se logar é:

![login](./static/assets/login.png)

A tela para se registrar é:

![cadastro](./static/assets/cadastro.png)

## Transações

### Adicionar, Visualizar e Gerenciar

A aplicação permite que os usuários adicione, visualize e gerencie suas transações.

A tela para visualizar principal é:

![adicionar](./static/assets/adicionar.png)

### Extrato

A aplicação permite que os usuários visualize o extrato de suas transações.

A tela para visualizar extrato é:

![extrato](./static/assets/extrato.png)

### Relatórios

A aplicação permite que os usuários gerem relatórios financeiros.

A tela para gerar relatórios é:

![relatorios](./static/assets/relatorios.png)

# MyFinances Backend

## Funcionalidades

- Autenticação de usuário (login e registro)
- Adicionar, visualizar e gerenciar transações financeiras
- Gerar relatórios financeiros
- Design responsivo para melhor experiência do usuário em vários dispositivos

## Requisitos

- Python 3.6+
- Flask
- Outras dependências especificadas em `requirements.txt`

## Configuração

### Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/EliasVRG/myFinances.git
    cd myfinances
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate   # No Windows: venv\Scripts\activate
    ```

3. Instale os pacotes necessários:
    ```bash
    pip install -r requirements.txt
    ```

### Configuração

Certifique-se de que o arquivo de configuração `users.json` e o diretório de transações `./extrato/` com `transactions.json` existam no diretório raiz do projeto.

### Executando a Aplicação

Inicie a aplicação Flask:
```bash
python app.py
```
A aplicação estará disponível em `http://localhost:8067/`.

## Estrutura do Projeto

```
myfinances/
│
├── app.py                      # Arquivo principal da aplicação
├── templates/                  # Modelos HTML
│   ├── index.html              # Modelo da página inicial
│   ├── login.html              # Modelo da página de login
│   ├── cadastro.html           # Modelo da página de registro
│   ├── extract.html            # Modelo da página de extrato
│   ├── reports.html            # Modelo da página de relatórios
│   └── navegacao.html          # Modelo da barra de navegação
├── static/                     # Arquivos estáticos (CSS, JS, imagens)
│   ├── style.css               # Estilos personalizados
│   ├── assets/                 # Imagens
│   │   └── dragao.png
├── users.json                  # Arquivo de dados dos usuários
└── extrato/                    # Diretório de transações
    └── transactions.json       # Arquivo de dados das transações
```

## Endpoints da API

### Autenticação

#### `GET /authentication`

Renderiza a página de login.

#### `POST /authentication`

Autentica o usuário e inicia uma sessão.

### Gerenciamento de Usuário

#### `GET /cadastro`

Renderiza a página de registro.

#### `POST /cadastro`

Registra um novo usuário.

### Transações

#### `GET /transactions`

Exibe as últimas 5 transações do usuário autenticado.

#### `POST /addTransaction`

Adiciona uma nova transação para o usuário autenticado.

### Relatórios

#### `GET /reports`

Gera e exibe relatórios financeiros baseados nas transações do usuário.

### Logout

#### `GET /logout`

Desloga o usuário e limpa a sessão.

## Funções Auxiliares

### `prepare_chart_data(transactions)`

Prepara os dados para gráficos processando as transações.

### `calculate_today_transactions(username)`

Calcula as entradas, saídas e o saldo atual do dia para um usuário.

### `is_authenticated()`

Verifica se o usuário está autenticado, verificando o token de sessão.

### `get_user_access()`

Obtém o nível de acesso do usuário autenticado.

### `load_users()`

Carrega os usuários a partir de `users.json`.

### `save_users(users)`

Salva os usuários em `users.json`.

### `get_last_5_transactions(username)`

Obtém as últimas 5 transações de um usuário.

### `get_transactions(username)`

Obtém todas as transações de um usuário.

### `load_transactions()`

Carrega as transações a partir de `transactions.json`.

### `save_transactions(transactions)`

Salva as transações em `transactions.json`.

## Gerenciamento de Sessão

- Tokens de sessão são gerados após a autenticação bem-sucedida e armazenados em cookies.
- Tokens de sessão são mapeados para nomes de usuário e níveis de acesso no dicionário `sessions`.

## Considerações de Segurança

- Certifique-se de validar e sanitizar corretamente as entradas do usuário para prevenir vulnerabilidades de segurança.
- Proteja dados e credenciais sensíveis.
- Implemente HTTPS para comunicação segura.

## Contribuição

Sinta-se à vontade para contribuir com este projeto, enviando problemas ou pull requests. Para mudanças maiores, por favor, abra um problema primeiro para discutir o que você gostaria de mudar.
