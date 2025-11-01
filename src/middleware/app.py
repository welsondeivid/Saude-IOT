import datetime
import requests
from typing import Dict, Any, List
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Configuração do backend
BACKEND_URL = "http://localhost:8000"  # URL do backend FastAPI

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Neighborhood(db.Model):
    __tablename__ = 'neighborhood'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)

    measurements = db.relationship('Measurement', back_populates='neighborhood', cascade='all, delete-orphan')


class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)

    clima = db.Column(db.JSON, nullable=True)
    qualidade_do_ar = db.Column(db.JSON, nullable=True)
    qualidade_da_agua = db.Column(db.JSON, nullable=True)
    riscos = db.Column(db.JSON, nullable=True)

    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'), nullable=False)
    neighborhood = db.relationship('Neighborhood', back_populates='measurements')

    __table_args__ = (
        db.UniqueConstraint('neighborhood_id', 'timestamp', name='uq_neigh_time'),
    )


@app.route('/')
def index():
    return jsonify({"msg": "Middleware ativo. Use POST /ingest para enviar dados para o backend."})


def _parse_timestamp(value: str) -> datetime.datetime:
    # Accept ISO8601 with optional 'Z' suffix
    if isinstance(value, str):
        v = value.replace('Z', '+00:00')
        try:
            return datetime.datetime.fromisoformat(v)
        except ValueError:
            pass
    raise ValueError('timestamp inválido, use ISO 8601 (ex.: 2025-10-20T14:30:00Z)')


def _ensure_neighborhood(name: str) -> Neighborhood:
    nb = Neighborhood.query.filter_by(name=name).first()
    if nb:
        return nb
    nb = Neighborhood(name=name)
    db.session.add(nb)
    db.session.flush()  # get id without full commit
    return nb


@app.route('/ingest', methods=['POST'])
def ingest():
    """
    Recebe dados do IoT e repassa para o backend via requisição HTTP.
    """
    payload: Dict[str, Any] = request.get_json(silent=True) or {}
    if 'bairros' not in payload or not isinstance(payload['bairros'], dict):
        return jsonify({"msg": "Corpo inválido: esperado objeto com chave 'bairros'"}), 400

    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ3ZWxzb24iLCJleHAiOjE3NjIwMDEwMjR9.mODc3QWbE8Quw38J5UkTCXww-RJcEqwnlvFqlJQAHDk"
    try:
        # Faz requisição para o backend
        response = requests.post(
            f"{BACKEND_URL}/importar-dados/",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            timeout=30
        )
                
        if response.status_code == 200:
            return jsonify({
                "msg": "Dados enviados com sucesso para o backend",
                "backend_response": response.json()
            }), 201
        else:
            return jsonify({
                "msg": "Erro ao enviar dados para o backend",
                "status_code": response.status_code,
                "error": response.text
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "msg": "Erro de conexão com o backend",
            "error": "Backend não está disponível"
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "msg": "Timeout na requisição para o backend",
            "error": "Backend demorou muito para responder"
        }), 504
    except Exception as e:
        return jsonify({
            "msg": "Erro interno ao processar requisição",
            "error": str(e)
        }), 500


def _parse_day_to_dt(day: str) -> datetime.datetime:
    """Converte 'YYYY-MM-DD' para datetime em UTC (00:00)."""
    try:
        d = datetime.date.fromisoformat(day)
        return datetime.datetime(d.year, d.month, d.day, tzinfo=datetime.timezone.utc)
    except Exception:
        raise ValueError("dia inválido, use formato YYYY-MM-DD")


@app.route('/ingest_v2', methods=['POST'])
def ingest_v2():
    """
    Aceita o novo formato diário e repassa para o backend via requisição HTTP:
    {
      "bairros": {
        "Nome do Bairro": {
          "YYYY-MM-DD": {
            "clima": {...},
            "qualidade_do_ar": {...},
            "qualidade_da_agua": {...},
            "riscos": { "clima": [], "qualidade_do_ar": [], "qualidade_da_agua": [] }
          }
        }
      }
    }
    """
    payload: Dict[str, Any] = request.get_json(silent=True) or {}
    if 'bairros' not in payload or not isinstance(payload['bairros'], dict):
        return jsonify({"msg": "Corpo inválido: esperado objeto com chave 'bairros'"}), 400

    try:
        # Faz requisição para o backend
        response = requests.post(
            f"{BACKEND_URL}/importar-dados/",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify({
                "msg": "Dados enviados com sucesso para o backend (v2)",
                "backend_response": response.json()
            }), 201
        else:
            return jsonify({
                "msg": "Erro ao enviar dados para o backend (v2)",
                "status_code": response.status_code,
                "error": response.text
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "msg": "Erro de conexão com o backend",
            "error": "Backend não está disponível"
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "msg": "Timeout na requisição para o backend",
            "error": "Backend demorou muito para responder"
        }), 504
    except Exception as e:
        return jsonify({
            "msg": "Erro interno ao processar requisição",
            "error": str(e)
        }), 500


@app.route('/bairros', methods=['GET'])
def list_bairros():
    items = Neighborhood.query.order_by(Neighborhood.name.asc()).all()
    return jsonify([{"id": n.id, "name": n.name} for n in items])


@app.route('/bairros/<string:nome>/medicoes', methods=['GET'])
def list_medicoes(nome: str):
    nb = Neighborhood.query.filter_by(name=nome).first()
    if not nb:
        return jsonify({"msg": "Bairro não encontrado"}), 404

    start = request.args.get('start')
    end = request.args.get('end')
    q = Measurement.query.filter_by(neighborhood_id=nb.id).order_by(Measurement.timestamp.asc())
    try:
        if start:
            q = q.filter(Measurement.timestamp >= _parse_timestamp(start))
        if end:
            q = q.filter(Measurement.timestamp <= _parse_timestamp(end))
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

    data = [
        {
            "timestamp": m.timestamp.replace(tzinfo=datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
            "clima": m.clima,
            "qualidade_do_ar": m.qualidade_do_ar,
            "qualidade_da_agua": m.qualidade_da_agua,
        }
        for m in q.all()
    ]
    return jsonify({"bairro": nb.name, "registros": data})


@app.route('/riscos', methods=['GET'])
def riscos():
    """
    Retorna os dados no formato novo, agrupados por dia, para todos os bairros.
    Exatamente a estrutura:
    {
      "bairros": { "Nome": { "YYYY-MM-DD": { ... } } }
    }
    """
    result: Dict[str, Any] = {"bairros": {}}

    bairros = Neighborhood.query.all()
    for nb in bairros:
        dias: Dict[str, Any] = {}
        regs: List[Measurement] = (
            Measurement.query
            .filter_by(neighborhood_id=nb.id)
            .order_by(Measurement.timestamp.asc())
            .all()
        )
        for m in regs:
            # normaliza para data (UTC)
            ts = m.timestamp
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=datetime.timezone.utc)
            dia_str = ts.date().isoformat()
            dias[dia_str] = {
                "clima": m.clima,
                "qualidade_do_ar": m.qualidade_do_ar,
                "qualidade_da_agua": m.qualidade_da_agua,
                "riscos": m.riscos or {"clima": [], "qualidade_do_ar": [], "qualidade_da_agua": []},
            }
        result["bairros"][nb.name] = dias

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)