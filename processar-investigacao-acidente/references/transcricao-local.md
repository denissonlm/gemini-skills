# Transcrição local de oitivas

## Ferramenta instalada

Use o transcritor local em:

`/Users/denisson/Documents/Codex/tools/sesmt-transcription/transcribe.py`

O ambiente inclui o modelo Whisper `large-v3-turbo`, processamento em português e saída com marcas de tempo. Execute preferencialmente:

```bash
/Users/denisson/Documents/Codex/tools/sesmt-transcription/venv/bin/python \
  /Users/denisson/Documents/Codex/tools/sesmt-transcription/transcribe.py \
  CAMINHO_DA_MIDIA PREFIXO_DE_SAIDA
```

O modo padrão `--engine auto` tenta o modelo MLX local `whisper-large-v3-turbo` quando Metal estiver acessível e faz fallback para o Whisper Turbo em CPU quando a sessão estiver isolada. Para exigir um mecanismo, use `--engine mlx` ou `--engine cpu`.

## Regras de uso

- Trabalhe sobre uma cópia ou leia a mídia original sem modificá-la.
- Preserve os arquivos `.txt` e `.json` produzidos na área de trabalho do caso.
- Confira contra a gravação cada trecho que sustentar data, horário, dinâmica, agente, EPI, testemunha, atendimento, causa ou ação.
- Marque palavras duvidosas como `[inaudível]` ou `[transcrição incerta]`; não corrija por contexto.
- Havendo conflito entre áudio e transcrição, prevalece o áudio e a divergência deve ser registrada.
- Se a aceleração MLX/Metal estiver indisponível no ambiente, use a execução local em CPU com o mesmo modelo. Isso muda o tempo de processamento, não autoriza trocar por um modelo de menor fidelidade.
- A transcrição não é um documento oficial e nunca autoriza preencher campos ausentes por inferência.
