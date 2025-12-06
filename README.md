# Chatterbox TTS Português - RunPod Serverless

Template para geração de voz em **português brasileiro** usando o modelo fine-tuned `FearL0rd/Chatterbox-TTS-Portuguese`.

## Uso

Este endpoint é específico para português. Para outros idiomas, use o endpoint `chatterbox-serverless` (multilingual).

### Request

```json
{
  "input": {
    "text": "No princípio, Deus criou os céus e a terra.",
    "audio_ref_base64": "...",
    "cfg_weight": 0.5,
    "exaggeration": 0.5
  }
}
```

### Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| text | string | - | Texto em português (obrigatório) |
| audio_ref_url | string | - | URL do áudio de referência |
| audio_ref_base64 | string | - | Áudio de referência em base64 |
| cfg_weight | float | 0.5 | Peso do CFG (0.0 a 1.0) |
| exaggeration | float | 0.5 | Expressividade (0.0 a 1.0) |

### Response

```json
{
  "audio_base64": "...",
  "sample_rate": 24000,
  "duration_seconds": 5.2
}
```

## Modelo

- **Base:** Chatterbox TTS (Resemble AI)
- **Fine-tuned:** FearL0rd/Chatterbox-TTS-Portuguese
- **Datasets:** BRSpeech-TTS, portuguese-tts
- **Licença:** MIT

## Projeto

Parte do projeto **A Bíblia em Vídeos** - produção de ~700 vídeos bíblicos em 10 idiomas.
