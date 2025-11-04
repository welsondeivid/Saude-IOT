import tkinter as tk
from tkinter import messagebox
import threading
from .iot_simulator import IoTSimulator

class IoTSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador IoT")
        self.simulator = None

        # Campo bairros
        tk.Label(root, text="Bairros (separados por vírgula):").pack(pady=5)
        self.bairros_entry = tk.Entry(root, width=50)
        self.bairros_entry.pack(pady=5)

        # Campo intervalo
        tk.Label(root, text="Intervalo de envio (segundos):").pack(pady=5)
        self.intervalo_entry = tk.Entry(root, width=10)
        self.intervalo_entry.insert(0, "15")  # valor padrão
        self.intervalo_entry.pack(pady=5)

        # Campos de autenticação (username e senha)
        tk.Label(root, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(root, width=40)
        self.username_entry.pack(pady=2)

        tk.Label(root, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(root, width=40, show="*")
        self.password_entry.pack(pady=2)

        # Botões iniciar/parar
        self.start_button = tk.Button(root, text="Iniciar", command=self.iniciar_loop)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Parar", command=self.parar_loop, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Log
        self.log_text = tk.Text(root, height=15, width=60)
        self.log_text.pack(pady=10)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def iniciar_loop(self):
        bairros_text = self.bairros_entry.get()
        if not bairros_text.strip():
            tk.messagebox.showwarning("Atenção", "Informe pelo menos um bairro!")
            return
        bairros = bairros_text.split(",")

        try:
            intervalo = float(self.intervalo_entry.get())
        except ValueError:
            tk.messagebox.showwarning("Atenção", "Intervalo inválido!")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            tk.messagebox.showwarning("Atenção", "Informe usuário e senha!")
            return

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.simulator = IoTSimulator(bairros, intervalo=intervalo, username=username, password=password)

        self.thread = threading.Thread(target=self.simulator.loop_envio, args=(self.log,), daemon=True)
        self.thread.start()
        self.log(f"Loop iniciado com intervalo de {intervalo}s...")

    def parar_loop(self):
        if self.simulator:
            self.simulator.parar()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Loop parado.")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = IoTSimulatorGUI(root)
    root.mainloop()
