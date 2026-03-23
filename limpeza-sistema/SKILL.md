---
name: limpeza-sistema
description: Realiza a limpeza de arquivos temporários, caches, lixeira e gerencia o espaço local do OneDrive para liberar espaço em disco.
---

# Limpeza de Sistema Personalizada (Açotubo)

Esta skill permite ao Gemini realizar uma manutenção preventiva e corretiva no HD do usuário, focando em arquivos inúteis e otimizando o armazenamento local do OneDrive.

## Regras de Segurança (CRÍTICO)

- **NUNCA** remova ou modifique arquivos que contenham em seu caminho as palavras: `SESMT`, `Treinamento`, `NR`, `Qualidade`, `Investigação`, `Relatório`.
- **NUNCA** delete arquivos de documentos (`.docx`, `.xlsx`, `.pdf`, `.pptx`) sem autorização expressa, a menos que estejam em pastas de `Temp` ou `Lixeira`.
- A limpeza de vídeos de GoPro e CFTV deve ser feita preferencialmente movendo para a nuvem (`Online-only`) via comando `attrib +U`.

## Fluxo de Trabalho

1. **Diagnóstico:** Verifique o espaço livre e o tamanho das pastas temporárias e lixeira.
2. **Confirmação:** Informe ao usuário quanto espaço pode ser liberado e peça autorização.
3. **Execução:** Utilize o script PowerShell fornecido na skill.

## Recursos Disponíveis

### Scripts

- `scripts/limpeza_segura.ps1`: Script PowerShell principal para automação da limpeza.
  - Parâmetros recomendados: `-ForceOneDriveCloudOnly` (para mover arquivos pesados para a nuvem).

### Exemplos de Uso

- "Me ajuda a limpar meu HD?" -> Execute o diagnóstico e sugira o uso da skill.
- "Libera espaço no meu OneDrive" -> Use a função de Online-only nos arquivos pesados da pasta `Organizar`.
- "Limpa os temporários e caches" -> Execute o script com os switches correspondentes.
