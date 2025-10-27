import os
import logging
import grpc
import requests
from concurrent import futures
from google.protobuf import struct_pb2

# Stubs locais gerados pelo protoc
import saude_pb2_grpc
import saude_pb2

FONTE_URL = os.getenv("RELATORIO_URL", "http://127.0.0.1:8000/relatorio-diario")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")

SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/json"})

class RelatorioService(saude_pb2_grpc.RelatorioServiceServicer):
    def ObterRelatorioDiario(self, request, context):
        logging.info(f"Buscando relatório em: {FONTE_URL}")
        try:
            resp = SESSION.get(FONTE_URL, timeout=10)
            logging.info(f"HTTP {resp.status_code} de {resp.url} (content-type={resp.headers.get('content-type')})")
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            body_preview = resp.text[:300].replace("\n", " ")
            logging.error(f"Resposta não é JSON. Trecho: {body_preview}")
            context.abort(grpc.StatusCode.DATA_LOSS, "Resposta não é JSON válido")
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha HTTP: {e}")
            context.abort(grpc.StatusCode.UNAVAILABLE, f"Falha ao buscar HTTP: {e}")

        s = struct_pb2.Struct()
        s.update(data)
        logging.info("Relatório obtido e repassado via gRPC.")
        return s

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    saude_pb2_grpc.add_RelatorioServiceServicer_to_server(RelatorioService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info(f"gRPC escutando em :50051; fonte={FONTE_URL}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()