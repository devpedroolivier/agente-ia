from app.remetente import enviar_resposta_padrao

def test_enviar_resposta_padrao_ceo():
    resposta = enviar_resposta_padrao("5511999999999", "relatorio 1 dia santana")
    assert isinstance(resposta, dict)
    assert "imagem" in resposta
    assert "mensagem" in resposta

    if resposta["imagem"]:
        assert resposta["imagem"].endswith(".png")
    else:
        print("⚠️ Sem imagem gerada — provavelmente dados vazios.")


def test_enviar_resposta_padrao_setor():
    resposta = enviar_resposta_padrao("5511999999999", "relatorio 3 dias setor 028")
    assert isinstance(resposta, dict)
    assert "imagem" in resposta
    assert "mensagem" in resposta

def test_comando_invalido():
    resposta = enviar_resposta_padrao("5511999999999", "gostaria de saber dados")
    assert isinstance(resposta, dict)
    assert "mensagem" in resposta
    assert "não entendi" in resposta["mensagem"].lower()
