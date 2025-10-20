from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from .database import engine, get_db

# Cria as tabelas no banco de dados (SQLite) se elas não existirem
models.Base.metadata.create_all(bind=engine) 

# ----------------------------------------------------------------------
# FUNÇÕES DE PROCESSAMENTO E CÁLCULO (LÓGICA DE NEGÓCIO)
# @ IKEL
# ----------------------------------------------------------------------
def calcular_medias_diarias(db: Session):
    # A consulta usa o SQLAlchemy para construir uma query SQL complexa de forma segura.
    resultados_consulta = (
        db.query(
            models.Bairro.nome.label("nome_bairro"),
            func.date(models.Medicao.data_hora).label("data"), # Extrai apenas a data do timestamp
            models.Indicador.nome.label("nome_indicador"),
            models.Indicador.id_categoria.label("id_categoria"),
            func.avg(models.ValorMedido.valor).label("media_valor") # Calcula a média do valor
        )
        .join(models.Medicao, models.Bairro.id_bairro == models.Medicao.id_bairro)
        .join(models.ValorMedido, models.Medicao.id_medicao == models.ValorMedido.id_medicao)
        .join(models.Indicador, models.ValorMedido.id_indicador == models.Indicador.id_indicador)
        .group_by("nome_bairro", "data", "nome_indicador", "id_categoria") # Agrupa os dados para o cálculo da média
        .order_by("nome_bairro", "data") # Ordena o resultado para clareza
        .all() # Executa a consulta e retorna todos os resultados
    )
    return resultados_consulta

app = FastAPI(title="IoT Microservice API")

# --- Configuração CORS (Essencial para o Frontend React) ---
# Permite que o frontend (ex: rodando na porta 3000) acesse o backend
origins = [
    "http://localhost:3000", # Adicione a porta que o React for usar
    "http://127.0.0.1:3000",
    # Adicione aqui o domínio do front em produção, se tiver
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# FUNÇÃO AUXILIAR PARA ANÁLISE DE RISCOS
# @ IKEL
# ----------------------------------------------------------------------
def inferir_riscos(dados_diarios: dict):
    # Recebe os dados médios de um dia e retorna um dicionário com os riscos inferidos.
    riscos = {
        "clima": [],
        "qualidade_do_ar": [],
        "qualidade_da_agua": []
    }

    # As chaves .get(nome, 0) são uma forma segura de acessar os valores, 
    # retornando 0 se a chave não existir.
    
    # --- Regras para Qualidade da Água ---
    if dados_diarios['qualidade_da_agua'].get('coliformes_totais', 0) > 500:
        riscos['qualidade_da_agua'].append("Contaminação por coliformes")
    if dados_diarios['qualidade_da_agua'].get('turbidez', 0) > 5.0:
        riscos['qualidade_da_agua'].append("Turbidez alta")

    # --- Regras para Qualidade do Ar ---
    if dados_diarios['qualidade_do_ar'].get('material_particulado_pm25', 0) > 75.0:
        riscos['qualidade_do_ar'].append("PM2.5 moderado")
    if dados_diarios['qualidade_do_ar'].get('monoxido_carbono', 0) > 5.0:
        riscos['qualidade_do_ar'].append("CO elevado — risco de intoxicação")

    # --- Regra Padrão ---
    # Se nenhuma regra de risco para o clima for acionada, adiciona uma mensagem padrão.
    if not riscos['clima']:
        riscos['clima'].append("Condições climáticas normais")
        
    return riscos

# ----------------------------------------------------------------------
# ENDPOINT DE IMPORTAÇÃO (INGESTÃO DOS DADOS DO JSON)
# @ ELIS
# ----------------------------------------------------------------------
@app.post("/importar-dados/")
def importar_dados_bairros(dados: schemas.DadosBairroSchema, db: Session = Depends(get_db)):
    """
    Recebe os dados de saúde urbana dos bairros, valida com os schemas
    e insere de forma estruturada no banco de dados.
    """
    
    # 1. Itera sobre cada bairro e sua lista de medições no JSON recebido
    for nome_bairro, medicoes_list in dados.bairros.items():

        # 2. Encontra o bairro no banco de dados ou cria um novo se não existir
        bairro_db = db.query(models.Bairro).filter(models.Bairro.nome == nome_bairro).first()
        if not bairro_db:
            bairro_db = models.Bairro(nome=nome_bairro)
            db.add(bairro_db)
            db.commit()
            db.refresh(bairro_db)

        # 3. Itera sobre cada registro de medição (cada hora) para aquele bairro
        for medicao_item in medicoes_list:
            
            # 4. Cria o registro principal da "Medicao"
            nova_medicao = models.Medicao(
                id_bairro=bairro_db.id_bairro,
                data_hora=medicao_item.timestamp
            )
            db.add(nova_medicao)
            db.commit()
            db.refresh(nova_medicao)

            # Dicionário para facilitar a iteração sobre todas as categorias e indicadores
            all_data = {
                'clima': medicao_item.clima.model_dump(),
                'qualidade_do_ar': medicao_item.qualidade_do_ar.model_dump(),
                'qualidade_da_agua': medicao_item.qualidade_da_agua.model_dump()
            }

            # 5. Itera sobre cada indicador (ex: temperatura_ar) e seu valor
            for nome_categoria, indicadores in all_data.items():
                for nome_indicador, valor in indicadores.items():
                    
                    # 6. Busca o ID do indicador no banco (ex: busca por "temperatura_ar")
                    indicador_db = db.query(models.Indicador).filter(models.Indicador.nome == nome_indicador).first()
                    
                    if indicador_db:
                        # 7. Cria o registro do valor medido, associando à medição principal e ao indicador
                        novo_valor = models.ValorMedido(
                            id_medicao=nova_medicao.id_medicao,
                            id_indicador=indicador_db.id_indicador,
                            valor=valor
                        )
                        db.add(novo_valor)

    db.commit() # Salva todas as inserções de valores no banco de uma vez
    return {"status": "Dados importados com sucesso!"}

# ----------------------------------------------------------------------
# ENDPOINT DE EXPOSIÇÃO (Para o Frontend de Exibição)
# @ ELIS / IKEL
# ----------------------------------------------------------------------
@app.get("/relatorio-diario/")
def obter_relatorio_diario(db: Session = Depends(get_db)):
    """
    Endpoint principal que calcula as médias diárias dos indicadores por bairro,
    infere riscos e retorna um relatório completo.
    """
    # 1. Busca os dados já calculados do banco
    medias_calculadas = calcular_medias_diarias(db)

    # 2. Estrutura os dados no formato JSON desejado
    relatorio_final = {}
    for bairro, data, indicador, id_cat, media in medias_calculadas:
        data_str = data.strftime("%Y-%m-%d")

        # Cria as chaves do dicionário se não existirem
        relatorio_final.setdefault(bairro, {}).setdefault(data_str, {
            'clima': {}, 'qualidade_do_ar': {}, 'qualidade_da_agua': {}
        })

        # Mapeia o indicador para a categoria correta.
        # ASSUMINDO: id_categoria 1=Clima, 2=Qualidade do Ar, 3=Qualidade da Água
        categoria_map = {1: 'clima', 2: 'qualidade_do_ar', 3: 'qualidade_da_agua'}
        nome_categoria = categoria_map.get(id_cat, 'desconhecida')

        if nome_categoria != 'desconhecida':
            if indicador == 'coliformes_totais':
                relatorio_final[bairro][data_str][nome_categoria][indicador] = int(media)
            else:
                relatorio_final[bairro][data_str][nome_categoria][indicador] = round(media, 2)
            
    # 3. Adiciona a análise de riscos em cada registro diário
    for bairro, dias in relatorio_final.items():
        for dia, dados_diarios in dias.items():
            relatorio_final[bairro][dia]['riscos'] = inferir_riscos(dados_diarios)

    return {"bairros": relatorio_final}

# Rota de Status Simples
@app.get("/")
def read_root():
    return {"status": "API is running", "framework": "FastAPI"}
