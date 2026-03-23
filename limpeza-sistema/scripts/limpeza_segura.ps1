param(
    [switch]$ForceOneDriveCloudOnly = $true, # PADRÃO: Libera espaço do OneDrive (online-only)
    [switch]$ClearRecycleBin = $true,
    [switch]$ClearTemp = $true,
    [switch]$ClearBrowserCache = $true,
    [switch]$ClearCaptures = $true
)

Write-Host "--- Iniciando Limpeza Personalizada Açotubo (OneDrive Online-Only ativado) ---" -ForegroundColor Cyan

# 1. Lixeira
if ($ClearRecycleBin) {
    Write-Host "[1/5] Esvaziando Lixeira..."
    Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue
}

# 2. Arquivos Temporários
if ($ClearTemp) {
    Write-Host "[2/5] Limpando arquivos temporários do usuário..."
    Get-ChildItem -Path "$env:TEMP\*" -Recurse -ErrorAction SilentlyContinue | 
        Where-Object { $_.FullName -notmatch "SESMT|Treinamento|NR|Qualidade" } |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# 3. Caches de Navegador
if ($ClearBrowserCache) {
    Write-Host "[3/5] Limpando caches do Chrome e Edge..."
    $chrome = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*"
    $edge = "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache\*"
    Remove-Item -Path $chrome -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $edge -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. Gravações de Tela (Capturas)
if ($ClearCaptures) {
    Write-Host "[4/5] Limpando pasta de Capturas local (Videos\Captures)..."
    $captures = "$env:USERPROFILE\Videos\Captures\*"
    Remove-Item -Path $captures -Recurse -Force -ErrorAction SilentlyContinue
}

# 5. Gerenciamento de Espaço OneDrive (Açotubo)
if ($ForceOneDriveCloudOnly) {
    $oneDrivePath = "$env:USERPROFILE\OneDrive - Grupo Açotubo"
    if (Test-Path $oneDrivePath) {
        Write-Host "[5/5] Liberando espaço local no OneDrive (mantendo apenas na nuvem)..."
        # Aplica o atributo 'Online-only' (+U) de forma recursiva na raiz, mantendo a estrutura online
        # Este comando libera o espaço do HD, mas não remove os arquivos da nuvem.
        cmd /c "attrib +U /S /D ""$oneDrivePath\*"""
    }
}

Write-Host "`n--- Limpeza concluída com sucesso! ---" -ForegroundColor Green
$drive = Get-PSDrive C
Write-Host "Espaço disponível no Disco C: $([math]::Round($drive.Free / 1GB, 2)) GB"
