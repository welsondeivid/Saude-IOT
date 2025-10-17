# 🏙️ Saúde IoT — Monitoramento e Análise de Saúde Urbana

Projeto da disciplina **Sistemas Distribuídos**

---

## 📋 Descrição do Projeto

O **Saúde IoT** é um sistema distribuído voltado para a **análise de dados de saúde urbana**, com o objetivo de **auxiliar na formulação de políticas públicas** baseadas em evidências.

O sistema coleta, processa e analisa dados de **sensores IoT** e **fontes públicas** (como dados epidemiológicos, ambientais e socioeconômicos) em diferentes **regiões urbanas** — como bairros, distritos ou zonas da cidade.

A partir dessas informações, é possível identificar **tendências, correlações e alertas** sobre condições de saúde da população, qualidade do ar, temperatura, ruído e outros fatores que afetam o bem-estar urbano.

---

## 🎯 Objetivos

- Desenvolver uma **arquitetura distribuída** para processamento de dados IoT.
- Aplicar conceitos de **Sistemas Distribuídos** como mensageria, replicação, tolerância a falhas e distribuição de carga.
- Analisar indicadores de saúde e ambiente por **região urbana**.
- Gerar **insights** que orientem **gestores públicos** na tomada de decisões sobre políticas de saúde urbana.

# SAUDE-IOT: Backend Microsserviço (FastAPI + SQLite)

Este repositório contém o backend do projeto SAUDE-IOT, implementado em Python utilizando o framework **FastAPI** para construir uma API de alta performance. O serviço é responsável por receber dados periódicos (JSON) de sensores simulados, persistir as medições no banco de dados **SQLite** e expor os dados processados para o frontend.

## Pré-requisitos

Certifique-se de ter o **Python 3.9+** instalado na sua máquina.

## Primeiros Passos

Siga as instruções abaixo para configurar e iniciar o servidor de desenvolvimento.

### 1. Clonar e Acessar o Repositório

Abra o seu terminal e execute os comandos para clonar o projeto e mudar para a branch correta do backend.

```bash
# 1. Clone o repositório
git clone https://"endereço do repositório"

# 2. Acesse a pasta do projeto
cd SAUDE-IOT

# 3. Mude para a branch do backend (se aplicável)
git checkout backend
```

### 2. Configurar e Ativar o Ambiente Virtual (Recomendado)

O uso de um ambiente virtual (venv) garante que as dependências do projeto não interfiram em outras instalações do Python.

# Crie o ambiente virtual
```bash
python -m venv venv
```

# Ative o ambiente virtual
# No Linux/macOS
```bash
source venv/bin/activate
```

# No Windows Powershell
```bash
.\venv\Scripts\activate
```

3. Instalar Dependências e Iniciar o Servidor
Após ativar o ambiente virtual, utilize o script start.sh para instalar todas as dependências listadas no requirements.txt e iniciar o servidor de desenvolvimento.

```bash
# Se estiver usando Linux/macOS, conceda permissão de execução ao script
chmod +x start.sh 

# Execute o script para instalar e iniciar o servidor
./start.sh
```

4. Verificação da API (Documentação Automática)
Após a execução do script, o servidor estará rodando.

Endpoint Principal (Status): O servidor estará acessível em http://127.0.0.1:8000.

Documentação Interativa (Swagger UI): Acesse http://127.0.0.1:8000/docs para explorar e testar todos os endpoints da API de forma interativa.