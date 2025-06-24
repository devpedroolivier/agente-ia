
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
    assert (
        "não entendi" in resposta["mensagem"].lower()
        or "nenhuma reclamação" in resposta["mensagem"].lower()
    )

def test_relatorio_valido_pirituba():
    resposta = enviar_resposta_padrao("5511999999999", "relatorio 1 dia pirituba")
    assert isinstance(resposta, dict)
    assert "mensagem" in resposta
    assert resposta["mensagem"]
    assert "imagem_bytes" in resposta or "imagem" in resposta
    assert resposta.get("imagem_bytes") or resposta.get("imagem")

def test_relatorio_multiplos_ceos():
    resposta = enviar_resposta_padrao("5511999999999", "relatorio 2 dias pirituba pirituba")
    assert isinstance(resposta, dict) or isinstance(resposta, list)
    if isinstance(resposta, list):
        for r in resposta:
            assert "mensagem" in r
            assert "imagem_bytes" in r or "imagem" in r
    else:
        assert "mensagem" in resposta
        assert "imagem_bytes" in resposta or "imagem" in resposta
