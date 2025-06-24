
from app.remetente import enviar_resposta_padrao

def test_ajuda():
    resposta = enviar_resposta_padrao("5511999999999", "ajuda")
    assert isinstance(resposta, dict)
    assert "mensagem" in resposta
    assert "comandos disponíveis" in resposta["mensagem"].lower()

def test_comando_invalido():
    resposta = enviar_resposta_padrao("5511999999999", "gostaria de saber dados")
    assert isinstance(resposta, dict)
    assert "mensagem" in resposta
    msg = resposta["mensagem"].lower()
    assert any(
        termo in msg for termo in [
            "não entendi",
            "nenhuma reclamação",
            "resumo das reclamações"
        ]
    )

def test_relatorio_valido_pirituba():
    resposta = enviar_resposta_padrao("5511999999999", "relatorio 1 dia pirituba")
    assert isinstance(resposta, dict)
    assert "mensagem" in resposta
    assert resposta["mensagem"]
    assert any(k in resposta for k in ["imagem_bytes", "imagem"]) or "nenhuma reclamação" in resposta["mensagem"].lower()

def test_relatorio_multiplos_ceos():
    resposta = enviar_resposta_padrao("5511999999999", "relatorio 2 dias pirituba pirituba")
    assert isinstance(resposta, dict) or isinstance(resposta, list)
    if isinstance(resposta, list):
        for r in resposta:
            assert "mensagem" in r
            assert "imagem_bytes" in r or "imagem" in r or "nenhuma reclamação" in r["mensagem"].lower()
    else:
        assert "mensagem" in resposta
        assert "imagem_bytes" in resposta or "imagem" in resposta or "nenhuma reclamação" in resposta["messagem"].lower()
