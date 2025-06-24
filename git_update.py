import subprocess

def executar_comando(comando):
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    print(resultado.stdout)
    if resultado.stderr:
        print("⚠️", resultado.stderr)

def main():
    mensagem = input("Digite a mensagem do commit: ").strip()
    if not mensagem:
        print("❌ Commit cancelado. Mensagem vazia.")
        return

    print("\n🚀 Adicionando arquivos modificados...")
    executar_comando("git add .")

    print("📝 Realizando commit...")
    executar_comando(f'git commit -m "{mensagem}"')

    print("🔄 Fazendo pull com rebase para sincronizar...")
    executar_comando("git pull --rebase")

    print("☁️ Enviando para o repositório remoto...")
    executar_comando("git push")

    print("✅ Processo concluído.")

if __name__ == "__main__":
    main()
