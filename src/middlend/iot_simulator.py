import time
import requests
from .data_generator import gerar_bairro

API_URL = "http://127.0.0.1:8000/importar-dados/"

class IoTSimulator:
    def __init__(self, bairros, intervalo=15):
        self.bairros = [b.strip() for b in bairros]
        self.intervalo = intervalo
        self.loop_ativo = False

    def montar_payload(self):
        return {"bairros": {bairro: [gerar_bairro(bairro)] for bairro in self.bairros}}

    def enviar_dados(self):
        payload = self.montar_payload()
        try:
            response = requests.post(API_URL, json=payload)
            return response.status_code, response.text
        except requests.RequestException as e:
            return None, str(e)

    def loop_envio(self, log_func=print):
        self.loop_ativo = True
        while self.loop_ativo:
            status, msg = self.enviar_dados()
            if status == 200:
                log_func("Dados enviados com sucesso!")
            elif status is not None:
                log_func(f"Erro: {status} - {msg}")
            else:
                log_func(f"Falha na conexão: {msg}")
            time.sleep(self.intervalo)

    def parar(self):
        self.loop_ativo = False
