import os
import shutil
import subprocess
from datetime import datetime
import sys

# Caminho de origem: onde estão os arquivos atualizados
origem = r"C:\Users\Pedri\Downloads"

# Caminho do repositório local clonado
repositorio = r"C:\Users\Pedri\agente-ia"
destino = os.path.join(repositorio, "data")

# ⚠️ Remove a pasta 'data' antiga se existir localmente
if os.path.exists(destino):
    shutil.rmtree(destino)
    print("📂 Pasta 'data' antiga removida.")

# Cria nova pasta 'data'
os.makedirs(destino, exist_ok=True)

# Localiza o arquivo .xlsx mais recente
arquivos = [os.path.join(origem, f) for f in os.listdir(origem) if f.endswith(".xlsx")]

if not arquivos:
    print("🚫 Nenhum arquivo .xlsx encontrado na pasta de origem!")
    sys.exit(1)

mais_recente = max(arquivos, key=os.path.getmtime)

# Copia o arquivo mais recente para a nova pasta 'data'
shutil.copy(mais_recente, destino)
print(f"✅ Arquivo copiado: {os.path.basename(mais_recente)}")

# Git remove da pasta antiga no repositório (marca para exclusão no controle de versão)
subprocess.run(["git", "rm", "-r", "--cached", "data"], cwd=repositorio)
print("🗑️ Pasta 'data' marcada para exclusão no Git.")

# Git add da nova pasta
subprocess.run(["git", "add", "./data"], cwd=repositorio)

# Git commit e push automático com rebase
commit_message = f"Atualiza dados {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
subprocess.run(["git", "commit", "-m", commit_message], cwd=repositorio)
subprocess.run(["git", "pull", "--rebase"], cwd=repositorio)
subprocess.run(["git", "push"], cwd=repositorio)

print("🚀 Dados enviados ao repositório remoto com sucesso.")
