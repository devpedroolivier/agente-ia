import pytest
import requests
from unittest.mock import patch
from app.remetente import enviar_texto, enviar_imagem

@patch("app.remetente.requests.post")
def test_enviar_texto(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = "Success"
    response = enviar_texto("5511999999999", "Teste de texto")
    mock_post.assert_called()
    assert response is None  # função não retorna valor

@patch("app.remetente.requests.post")
def test_enviar_imagem(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"id": "media-id"}
    mock_post.return_value.text = "Success"
    fake_buffer = b"fake_image_data"
    response = enviar_imagem("5511999999999", fake_buffer)
    mock_post.assert_called()
    assert response is None
