"""
Chatterbox TTS Português - RunPod Serverless Handler
=====================================================
Template customizado para o projeto "A Bíblia em Vídeos"

IMPORTANTE: Usa o modelo PORTUGUÊS treinado com áudios brasileiros!
Modelo: FearL0rd/Chatterbox-TTS-Portuguese

Autor: Projeto Bíblia em Vídeos
Data: 2025-12-06
"""

import runpod
import torch
import torchaudio
import base64
import io
import os
import tempfile
import requests

# Variável global para o modelo (carrega uma vez, reutiliza)
MODEL = None

# Modelo português treinado com áudios brasileiros
PORTUGUESE_MODEL = "FearL0rd/Chatterbox-TTS-Portuguese"

def get_model():
    """Carrega o modelo Chatterbox PORTUGUÊS (singleton pattern)"""
    global MODEL
    if MODEL is None:
        print(f"Carregando modelo Chatterbox PORTUGUES: {PORTUGUESE_MODEL}")
        from chatterbox.tts import ChatterboxTTS
        device = "cuda" if torch.cuda.is_available() else "cpu"
        MODEL = ChatterboxTTS.from_pretrained(PORTUGUESE_MODEL, device=device)
        print(f"Modelo PORTUGUES carregado no dispositivo: {device}")
    return MODEL


def download_audio(url: str, timeout: int = 60) -> bytes:
    """Baixa áudio de uma URL"""
    print(f"Baixando audio de: {url[:50]}...")
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    print(f"Download completo: {len(response.content)} bytes")
    return response.content


def save_temp_audio(audio_data: bytes, suffix: str = ".mp3") -> str:
    """Salva áudio em arquivo temporário"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(audio_data)
    temp_file.close()
    return temp_file.name


def generate_speech(
    text: str,
    audio_ref_path: str,
    cfg_weight: float = 0.5,
    exaggeration: float = 0.5
) -> bytes:
    """
    Gera áudio com voice cloning PORTUGUÊS
    """
    model = get_model()

    print(f"Gerando audio PORTUGUES...")
    print(f"   Texto: {text[:50]}...")
    print(f"   cfg_weight: {cfg_weight}")
    print(f"   exaggeration: {exaggeration}")

    wav = model.generate(
        text=text,
        audio_prompt_path=audio_ref_path,
        cfg_weight=cfg_weight,
        exaggeration=exaggeration
    )

    buffer = io.BytesIO()
    torchaudio.save(buffer, wav, model.sr, format="wav")
    buffer.seek(0)

    print(f"Audio gerado: {buffer.getbuffer().nbytes} bytes")
    return buffer.read()


def handler(event: dict) -> dict:
    """
    Handler principal do RunPod Serverless

    Input:
    {
        "input": {
            "text": "No princípio, Deus criou os céus e a terra.",
            "audio_ref_url": "https://..." ou "audio_ref_base64": "...",
            "cfg_weight": 0.5,
            "exaggeration": 0.5
        }
    }
    """
    try:
        input_data = event.get("input", {})

        text = input_data.get("text")
        if not text:
            return {"error": "Campo 'text' é obrigatório"}

        audio_ref_url = input_data.get("audio_ref_url")
        audio_ref_base64 = input_data.get("audio_ref_base64")

        if not audio_ref_url and not audio_ref_base64:
            return {"error": "Forneça 'audio_ref_url' ou 'audio_ref_base64'"}

        cfg_weight = float(input_data.get("cfg_weight", 0.5))
        exaggeration = float(input_data.get("exaggeration", 0.5))

        temp_audio_path = None
        try:
            if audio_ref_url:
                audio_data = download_audio(audio_ref_url)
                suffix = ".mp3" if ".mp3" in audio_ref_url.lower() else ".wav"
                temp_audio_path = save_temp_audio(audio_data, suffix)
            else:
                audio_data = base64.b64decode(audio_ref_base64)
                temp_audio_path = save_temp_audio(audio_data, ".mp3")

            output_audio = generate_speech(
                text=text,
                audio_ref_path=temp_audio_path,
                cfg_weight=cfg_weight,
                exaggeration=exaggeration
            )

            model = get_model()
            duration = len(output_audio) / (model.sr * 2)

            return {
                "audio_base64": base64.b64encode(output_audio).decode("utf-8"),
                "sample_rate": model.sr,
                "duration_seconds": round(duration, 2)
            }

        finally:
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)

    except Exception as e:
        print(f"Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


if __name__ == "__main__":
    print("Iniciando Chatterbox TTS PORTUGUES Serverless...")
    print(f"Modelo: {PORTUGUESE_MODEL}")
    runpod.serverless.start({"handler": handler})
