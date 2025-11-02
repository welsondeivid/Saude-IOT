from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

from . import models, schemas
from .database import engine, get_db, SessionLocal

# Cria as tabelas no banco de dados (SQLite) se elas não existirem
models.Base.metadata.create_all(bind=engine) 

# ======================================================================
# FUNÇÃO PARA POPULAR O BANCO DE DADOS NA INICIALIZAÇÃO (CORRIGIDA)
# ======================================================================
def popular_dados_iniciais(db: Session):
    # Apenas executa se a tabela Categoria estiver vazia
    if db.query(models.Categoria).count() == 0:
        print("Populando tabelas Categoria e Indicador...")

        # --- Cria as Categorias ---
        cat_clima = models.Categoria(nome="Clima")
        cat_ar = models.Categoria(nome="Qualidade do Ar")
        cat_agua = models.Categoria(nome="Qualidade da Agua")
        db.add_all([cat_clima, cat_ar, cat_agua])
        db.commit()

        # --- Cria os Indicadores ---
        # (Usa os objetos de categoria que acabamos de criar para obter os IDs)
        indicadores = [
            models.Indicador(nome="temperatura_ar", unidade_medida="°C", categoria=cat_clima),
            models.Indicador(nome="umidade_relativa", unidade_medida="%", categoria=cat_clima),
            models.Indicador(nome="precipitacao", unidade_medida="mm", categoria=cat_clima),
            models.Indicador(nome="cobertura_vegetal", unidade_medida="%", categoria=cat_clima),
            
            models.Indicador(nome="material_particulado_pm25", unidade_medida="µg/m³", categoria=cat_ar),
            models.Indicador(nome="monoxido_carbono", unidade_medida="ppm", categoria=cat_ar),

            models.Indicador(nome="ph_agua", unidade_medida="pH", categoria=cat_agua),
            models.Indicador(nome="turbidez", unidade_medida="NTU", categoria=cat_agua),
            models.Indicador(nome="coliformes_totais", unidade_medida="NMP/100ml", categoria=cat_agua),
            models.Indicador(nome="cloro_residual", unidade_medida="mg/L", categoria=cat_agua),
        ]
        db.add_all(indicadores)
        db.commit()
        print("Dados iniciais populados com sucesso!")

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

@app.on_event("startup")
def on_startup():
    # Cria uma nova sessão de DB apenas para a inicialização
    db = SessionLocal()
    try:
        popular_dados_iniciais(db)
    finally:
        # Fecha a sessão após o uso
        db.close()

# --- Configuração CORS (Essencial para o Frontend React) ---
# Permite que o frontend (ex: rodando na porta 3000) acesse o backend
origins = [
    "http://localhost:3000", # Adicione a porta que o React for usar
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    # Adicione aqui o domínio do front em produção, se tiver
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO
# ======================================================================

# Chave secreta para assinar o JWT (em um app de produção, use um segredo mais forte e carregue-o de uma variável de ambiente)
SECRET_KEY = "Vv2pLnqtvG8GOYeOPw6wHWG8f9PDKqP9xw9CeEDx4Wz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ======================================================================
# FUNÇÕES AUXILIARES DE AUTENTICAÇÃO
# ======================================================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# ======================================================================
# DEPENDÊNCIA PARA OBTER O USUÁRIO ATUAL
# ======================================================================

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# ======================================================================
# ROTA DE LOGIN (TOKEN)
# ======================================================================

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ======================================================================
# ROTA PARA CRIAR USUÁRIOS
# ======================================================================

@app.post("/users/", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me/", response_model=schemas.UserInDB)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

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
def importar_dados_bairros(
    dados: schemas.DadosBairroSchema, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # <- Adicione esta linha
):
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
def obter_relatorio_diario(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Endpoint principal que calcula as médias diárias dos indicadores por bairro,
    infere riscos e retorna um relatório completo.
    """
    # 1. (CORREÇÃO) Busca as categorias do banco para criar um mapa dinâmico.
    # Isso evita o erro de IDs fixos (hardcoded).
    categorias_db = db.query(models.Categoria).all()
    categoria_map = {
        cat.id_categoria: cat.nome.lower().replace(" ", "_") for cat in categorias_db
    } # Ex: {1: 'clima', 2: 'qualidade_do_ar'}

    # 2. Busca os dados já calculados do banco
    medias_calculadas = calcular_medias_diarias(db)

    # 3. Estrutura os dados no formato JSON desejado
    relatorio_final = {}
    for bairro, data, indicador, id_cat, media in medias_calculadas:
        data_str = data

        # Cria as chaves do dicionário se não existirem
        relatorio_final.setdefault(bairro, {}).setdefault(data_str, {
            'clima': {}, 'qualidade_do_ar': {}, 'qualidade_da_agua': {}
        })

        # Mapeia o indicador para a categoria correta usando o mapa dinâmico
        nome_categoria = categoria_map.get(id_cat, 'desconhecida')

        if nome_categoria != 'desconhecida':
            # Converte para inteiro se for o caso, senão arredonda para 2 casas decimais
            valor_final = int(media) if indicador == 'coliformes_totais' else round(media, 2)
            relatorio_final[bairro][data_str][nome_categoria][indicador] = valor_final
            
    # 4. Adiciona a análise de riscos em cada registro diário
    for bairro, dias in relatorio_final.items():
        for dia, dados_diarios in dias.items():
            relatorio_final[bairro][dia]['riscos'] = inferir_riscos(dados_diarios)

    return {"bairros": relatorio_final}
# Rota de Status Simples
@app.get("/")
def read_root():
    return {"status": "API is running", "framework": "FastAPI"}

