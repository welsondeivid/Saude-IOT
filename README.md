# 🏙️ Saúde IoT — Backend de Monitoramento e Análise de Saúde Urbana

Este repositório contém o backend do projeto **Saúde IoT**, uma API de microsserviço responsável por coletar, armazenar e analisar dados de saúde urbana.

## 📋 Visão Geral do Projeto

O **Saúde IoT** é um sistema distribuído que visa agregar dados de sensores IoT e fontes públicas para gerar insights que auxiliem gestores públicos na formulação de políticas de saúde.

Este backend é o componente central da arquitetura, responsável por:

1.  **Autenticar** usuários e dispositivos através de tokens JWT.
2.  **Receber** dados de medição enviados por dispositivos IoT.
3.  **Armazenar** os dados de forma estruturada em um banco de dados.
4.  **Processar** e **analisar** os dados para calcular médias diárias e inferir riscos.
5.  **Expor** os resultados através de um endpoint para ser consumido por um frontend de visualização.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.9+
* **Framework da API**: [FastAPI](https://fastapi.tiangolo.com/)
* **Banco de Dados**: [SQLite](https://www.sqlite.org/index.html)
* **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
* **Validação de Dados**: [Pydantic](https://docs.pydantic.dev/)
* **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
* Autenticação: JWT (JSON Web Tokens) com `python-jose`
* Criptografia de Senha: passlib com `bcrypt`

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e iniciar o servidor localmente.

### 1. Pré-requisitos
* Python 3.9 ou superior.
* Git.

### 2. Configuração do Ambiente

```bash
# 1. Clone o repositório
git clone [https://github.com/welsondeivid/Saude-IOT/](https://github.com/welsondeivid/Saude-IOT/)
cd Saude-IOT

# 2. Crie e ative um ambiente virtual (recomendado)
# No Windows:
python -m venv venv
.\venv\Scripts\activate

# No macOS/Linux:
python -m venv venv
source venv/bin/activate
```

### 3. Instalação e Inicialização

O projeto inclui dois scripts para facilitar a instalação e inicialização.

```bash
# No macOS/Linux, conceda permissão de execução primeiro:
chmod +x start.sh

# No Windows, instale as dependências e inicie o servidor:
./start.sh
```

Após isso, abra outra janela ou split o terminal, também precisa ser bash, para iniciar o simulador IOT
```bash
# No macOS/Linux, conceda permissão de execução primeiro:
chmod +x start.sh

# No Windows, instale as dependências e inicie o servidor:
./gui.sh
```


## 📖 Documentação da API
A API possui documentação interativa gerada automaticamente. Após iniciar o servidor, acesse:

Swagger UI: http://127.0.0.1:8000/docs

Lá você pode visualizar e testar todos os endpoints.

## 👨‍💻 Guia para Desenvolvedores
Esta seção detalha como os times de IoT e Frontend devem interagir com a API.

### 🔹 Para o Time de IoT (Enviando Dados)
Seu papel é enviar os dados coletados pelos sensores para o nosso endpoint de ingestão.

Endpoint: POST /importar-dados/

#### Formato do JSON:
Você deve enviar um JSON com a seguinte estrutura.
A chave principal bairros contém um dicionário, onde cada chave é o nome de um bairro.

json
```

{
  "bairros": {
    "Nome do Bairro": [
      {
        "timestamp": "2025-10-20T14:30:00Z",
        "clima": {
          "temperatura_ar": 25.5,
          "umidade_relativa": 68.0,
          "precipitacao": 0.0,
          "cobertura_vegetal": 55.2
        },
        "qualidade_do_ar": {
          "material_particulado_pm25": 30.1,
          "monoxido_carbono": 1.5
        },
        "qualidade_da_agua": {
          "ph_agua": 7.2,
          "turbidez": 1.8,
          "coliformes_totais": 150,
          "cloro_residual": 0.5
        }
      }
    ]
  }
}
```

### Observações:

- O timestamp deve estar no formato ISO 8601.

- Todos os campos numéricos são do tipo float, exceto coliformes_totais, que é um int.

Se os dados forem enviados corretamente, a API retornará:

json
```
{"status": "Dados importados com sucesso!"}
```

Com o código 200.

### 🔹 Para o Time de Frontend (Consumindo Dados)
Seu papel é buscar os dados processados para exibi-los em um dashboard.

Endpoint: GET /relatorio-diario/

#### Formato da resposta:
A API retornará um relatório consolidado com as médias diárias por bairro e uma análise de riscos.

json
```
{
  "bairros": {
    "Nome do Bairro": {
      "2025-10-20": {
        "clima": {
          "temperatura_ar": 26.1,
          "umidade_relativa": 70.5,
          "precipitacao": 0.1,
          "cobertura_vegetal": 55.2
        },
        "qualidade_do_ar": {
          "material_particulado_pm25": 45.8,
          "monoxido_carbono": 3.1
        },
        "qualidade_da_agua": {
          "ph_agua": 7.1,
          "turbidez": 2.5,
          "coliformes_totais": 300,
          "cloro_residual": 0.8
        },
        "riscos": {
          "clima": [
            "Condições climáticas normais"
          ],
          "qualidade_do_ar": [
            "PM2.5 moderado"
          ],
          "qualidade_da_agua": []
        }
      }
    }
  }
}
```

# Guia para Desenvolvedores
-------------------------

Com a implementação da autenticação, o fluxo de interação com a API mudou. Todas as rotas de dados agora são protegidas.

### 🔐 Fluxo de Autenticação (Obrigatório)

1.  **Crie um usuário**: Use o endpoint POST /users/ para registrar um novo usuário e senha.
    
2.  **Faça Login**: Envie o usuário e senha para o endpoint POST /token para receber um access\_token.
    
3.  **Acesse as Rotas Protegidas**: Inclua o token recebido no cabeçalho (Header) de todas as requisições futuras para as rotas de dados.
    
    *   **Header**: `Authorization: Bearer <SEU_TOKEN_AQUI>`
        

### Criando um Usuário

Para interagir com a API, primeiro você precisa de um usuário.

**Endpoint**: `POST /users/`

#### Formato do JSON:

JSON
```
{
  "username": "seu_usuario",
  "password": "sua_senha_segura"
}
```

Se a criação for bem-sucedida, a API retornará o nome de usuário criado com o código 200.

### 🔹 Obtendo um Token de Acesso (Login)

**Endpoint**: `POST /token`

Este endpoint usa o formato form-data (não JSON).

#### Formato do form-data:

*   username: seu\_usuario
    
*   password: sua\_senha\_segura
    

Se as credenciais estiverem corretas, a API retornará o token de acesso:

JSON
```
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",    "token_type": "bearer"  }   `
```
**Copie o valor de access\_token para usar nos passos seguintes.**

### 🔹 Para o Time de IoT (Enviando Dados)

Seu papel é enviar os dados coletados pelos sensores para o nosso endpoint de ingestão, **agora com autenticação**.

**Endpoint**: POST /importar-dados/

#### Requisitos:

*   **Header de Autenticação**: Authorization: Bearer
    
*   **Corpo da Requisição (JSON)**: O mesmo formato de antes.
    

Se os dados forem enviados corretamente, a API retornará:

JSON
```
{"status": "Dados importados com sucesso!"}
```

Com o código 200. Caso o token seja inválido ou não seja fornecido, a API retornará 401 Unauthorized.

### Para o Time de Frontend (Consumindo Dados)

Seu papel é buscar os dados processados para exibi-los em um dashboard, **agora com autenticação**.

**Endpoint**: GET /relatorio-diario/

#### Requisitos:

*   **Header de Autenticação**: `Authorization: Bearer`
    

A API retornará o relatório consolidado com as médias diárias por bairro e uma análise de riscos, no mesmo formato de antes. Caso o token seja inválido ou não seja fornecido, a API retornará 401 Unauthorized.
### Observações:

- O backend está configurado com CORS para permitir requisições vindas de http://localhost:3000.
Se o seu ambiente de desenvolvimento frontend usar uma porta diferente, avise o time de backend para adicioná-la à lista.

- A seção riscos é gerada com base em regras predefinidas no backend.
Uma lista vazia (como em qualidade_da_agua no exemplo) significa que nenhum risco foi identificado para aquela categoria no dia.
