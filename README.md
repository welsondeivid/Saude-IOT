# 🏙️ Saúde IoT — Backend de Monitoramento e Análise de Saúde Urbana

Este repositório contém o backend do projeto **Saúde IoT**, uma API de microsserviço responsável por coletar, armazenar e analisar dados de saúde urbana.

## 📋 Visão Geral do Projeto

O **Saúde IoT** é um sistema distribuído que visa agregar dados de sensores IoT e fontes públicas para gerar insights que auxiliem gestores públicos na formulação de políticas de saúde.

Este backend é o componente central da arquitetura, responsável por:
1.  **Receber** dados de medição enviados por dispositivos IoT.
2.  **Armazenar** os dados de forma estruturada em um banco de dados.
3.  **Processar** e **analisar** os dados para calcular médias diárias e inferir riscos.
4.  **Expor** os resultados através de um endpoint para ser consumido por um frontend de visualização.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.9+
* **Framework da API**: [FastAPI](https://fastapi.tiangolo.com/)
* **Banco de Dados**: [SQLite](https://www.sqlite.org/index.html)
* **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
* **Validação de Dados**: [Pydantic](https://docs.pydantic.dev/)
* **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)

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
