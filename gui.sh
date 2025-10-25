#!/bin/bash
# Script para iniciar a GUI do simulador IoT

# Vai para a pasta src
cd "$(dirname "$0")/src" || exit 1

# Executa a GUI
python -m middlend.gui
