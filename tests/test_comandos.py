from app.comandos import extrair_dias, interpretar_mensagem

def test_extrair_dias():
    assert extrair_dias("relatório 5 dias") == 5
    assert extrair_dias("relatório de hoje") == 1
    assert extrair_dias("sem número") == 1

def test_interpretar_mensagem():
    res = interpretar_mensagem("relatório setor 042 pirituba 3 dias")
    assert res["dias"] == 3
    assert res["setor"] == "042"
    assert res["polo"] == "p"

def test_interpretar_mensagem_sem_dias():
    res = interpretar_mensagem("relatório setor 042 pirituba")
    assert res["dias"] == 1
    assert res["polo"] == "p"

def test_interpretar_mensagem_sem_polo():
    res = interpretar_mensagem("relatório setor 042 3 dias")
    assert res["dias"] == 3
    assert res["polo"] is None

def test_interpretar_mensagem_com_erro():
    res = interpretar_mensagem("texto aleatório sem sentido")
    assert isinstance(res, dict)
    assert "dias" in res
