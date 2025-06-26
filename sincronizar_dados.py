import os
import shutil
import subprocess
from datetime import datetime

# Caminho de origem: onde estão os arquivos atualizados
origem = r"C:\Users\Pedri\Downloads"

# Caminho do repositório local clonado
repositorio = r"C:\Users\Pedri\OneDrive\Documentos\GitHub\agente-ia"
destino = os.path.join(repositorio, "data")

# ⚠️ Remove a pasta 'data' antiga se existir
if os.path.exists(destino):
    shutil.rmtree(destino)
    print("📂 Pasta 'data' antiga removida.")

# Cria nova pasta 'data'
os.makedirs(destino, exist_ok=True)

# Localiza o arquivo .xlsx mais recente
arquivos = [os.path.join(origem, f) for f in os.listdir(origem) if f.endswith(".xlsx")]
mais_recente = max(arquivos, key=os.path.getmtime)

# Copia o arquivo mais recente para a nova pasta 'data'
shutil.copy(mais_recente, destino)
print(f"✅ Arquivo copiado: {os.path.basename(mais_recente)}")

# Git commit e push automático
# Git commit e push automático com rebase
subprocess.run(["git", "add", "."], cwd=repositorio)
subprocess.run(["git", "commit", "-m", f"Atualiza dados {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], cwd=repositorio)
subprocess.run(["git", "pull", "--rebase"], cwd=repositorio)  # Adicionado
subprocess.run(["git", "push"], cwd=repositorio)

