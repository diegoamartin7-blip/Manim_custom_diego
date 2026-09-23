# ======================================================================
#  CALCULO 1 - PRIMER PARCIAL - 3 videos en un solo batch
#    Video 1: Probabilidad MUY ALTA  (sup/inf, Darboux, integrabilidad, eps-delta)
#    Video 2: Probabilidad ALTA      (continuidad, propiedades de la integral, Bolzano)
#    Video 3: Probabilidad MEDIA     (limites, Lipschitz, composicion, V/F, formulario)
#
#  Uso:   render_4k.bat   /   render_preview.bat
#         powershell -File render_all.ps1 -Mode 4k|1080|preview
#                    [-Video all|1|2|3] [-MaxParallel 16] [-Only V1_05_DarbouxParcial,V2_03_ContPractico]
#
#  - La lista de escenas se lee del SCENE_ORDER de cada archivo .py
#    (si agregas o sacas una escena, no hay que tocar este script).
#  - Todas las escenas corren EN PARALELO, cada una con su propia carpeta
#    media_<escena> (no se pisan los temporales).
#  - Antes de cada escena se borra su carpeta (nada de cache viejo).
#  - Al terminar cada escena se borran sus partial_movie_files.
#  - Al final, ffmpeg une cada video por separado.
#  - Con -Only re-renderizas solo las que fallaron y se re-unen los videos.
# ======================================================================
param(
    [ValidateSet("4k", "1080", "preview")][string]$Mode = "4k",
    [ValidateSet("all", "1", "2", "3")][string]$Video = "all",
    [int]$MaxParallel = 16,
    [string[]]$Only = @()
)
Set-Location $PSScriptRoot
$ErrorActionPreference = "Continue"
# Con "powershell -File", "-Only A,B" llega como un solo texto: lo separo a mano.
$Only = @($Only | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })

function Get-SceneOrder($file) {
    $src = Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot "$file.py")
    $m = [regex]::Match($src, 'SCENE_ORDER\s*=\s*\[(.*?)\]', 'Singleline')
    if (-not $m.Success) { Write-Host "No encontre SCENE_ORDER en $file.py" -ForegroundColor Red; exit 1 }
    return @([regex]::Matches($m.Groups[1].Value, '"([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
}

$videos = [ordered]@{
    "1" = @{ file = "v1_muy_alta"; out = "C1_V1_Probabilidad_Muy_Alta" }
    "2" = @{ file = "v2_alta";     out = "C1_V2_Probabilidad_Alta" }
    "3" = @{ file = "v3_media";    out = "C1_V3_Probabilidad_Media" }
}
foreach ($k in @($videos.Keys)) { $videos[$k].scenes = Get-SceneOrder $videos[$k].file }
$sel = if ($Video -eq "all") { @("1","2","3") } else { @($Video) }

switch ($Mode) {
    "4k"      { $q = "-qk"; $tag = "2160p60" }
    "1080"    { $q = "-qh"; $tag = "1080p60" }
    "preview" { $q = "-ql"; $tag = "480p15" }
}

# ---------- 1) Detectar manim y ffmpeg ----------
function Test-Cmd($exe, $pre) {
    try { & $exe @pre --version *> $null; return ($LASTEXITCODE -eq 0) } catch { return $false }
}
$exe = $null; $pre = @()
if     (Test-Cmd "manim"  @())             { $exe = "manim";  $pre = @() }
elseif (Test-Cmd "python" @("-m","manim")) { $exe = "python"; $pre = @("-m","manim") }
elseif (Test-Cmd "py"     @("-m","manim")) { $exe = "py";     $pre = @("-m","manim") }
if (-not $exe) { Write-Host "No encontre Manim (manim / python -m manim / py -m manim). pip install manim" -ForegroundColor Red; exit 1 }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "No encontre ffmpeg en el PATH.  winget install ffmpeg  y abri una terminal nueva." -ForegroundColor Red; exit 1
}

# ---------- 2) Espacio en disco ----------
$drive = (Get-Item $PSScriptRoot).PSDrive
$freeGB = [math]::Round((Get-PSDrive $drive.Name).Free / 1GB, 1)
$needGB = if ($Mode -eq "4k") { 40 } elseif ($Mode -eq "1080") { 12 } else { 3 }
if ($freeGB -lt $needGB) {
    Write-Host "Poco espacio en $($drive.Name): ($freeGB GB libres, conviene tener $needGB GB)." -ForegroundColor Yellow
    Write-Host "Sigo igual; si falla por disco, libera espacio y usa -Only." -ForegroundColor Yellow
}

# ---------- 3) Armar la lista de trabajos ----------
$jobs = @()
foreach ($v in $sel) {
    foreach ($s in $videos[$v].scenes) {
        if ($Only.Count -eq 0 -or $Only -contains $s) { $jobs += @{ v = $v; s = $s; f = $videos[$v].file } }
    }
}
Write-Host "Manim: $exe $($pre -join ' ')  |  Modo: $Mode ($tag)  |  Escenas: $($jobs.Count)  |  Paralelo: $MaxParallel  |  Disco libre: $freeGB GB" -ForegroundColor Cyan

$logDir = Join-Path $PSScriptRoot "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$start = Get-Date
$procs = @{}
$cleaned = @{}

function Clean-Partials($s) {
    $pm = Join-Path $PSScriptRoot "media_$s\videos"
    if (Test-Path $pm) {
        Get-ChildItem $pm -Recurse -Directory -Filter "partial_movie_files" -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ---------- 4) Lanzar en paralelo ----------
foreach ($j in $jobs) {
    while ((@($procs.Values | Where-Object { -not $_.HasExited })).Count -ge $MaxParallel) {
        foreach ($k in @($procs.Keys)) { if ($procs[$k].HasExited -and -not $cleaned[$k]) { Clean-Partials $k; $cleaned[$k] = $true } }
        Start-Sleep -Seconds 2
    }
    $s = $j.s
    $md = Join-Path $PSScriptRoot "media_$s"
    if (Test-Path $md) { Remove-Item $md -Recurse -Force -ErrorAction SilentlyContinue }
    $margs = $pre + @("render", $q, "--disable_caching", "--media_dir", "media_$s", "$($j.f).py", $s)
    $p = Start-Process -FilePath $exe -ArgumentList $margs -WindowStyle Hidden -PassThru `
         -RedirectStandardOutput (Join-Path $logDir "$s.out.txt") `
         -RedirectStandardError  (Join-Path $logDir "$s.err.txt")
    $null = $p.Handle
    $procs[$s] = $p
    Write-Host "  lanzada  $s" -ForegroundColor DarkGray
}

# ---------- 5) Esperar con progreso ----------
while ((@($procs.Values | Where-Object { -not $_.HasExited })).Count -gt 0) {
    foreach ($k in @($procs.Keys)) { if ($procs[$k].HasExited -and -not $cleaned[$k]) { Clean-Partials $k; $cleaned[$k] = $true } }
    $done = (@($procs.Values | Where-Object { $_.HasExited })).Count
    $min = [int]((Get-Date) - $start).TotalMinutes
    Write-Host ("  {0}/{1} escenas listas  ({2} min)" -f $done, $jobs.Count, $min)
    Start-Sleep -Seconds 20
}
foreach ($k in @($procs.Keys)) { if (-not $cleaned[$k]) { Clean-Partials $k } }

# ---------- 6) Verificar y unir cada video ----------
$bad = @()
foreach ($j in $jobs) {
    $mp4 = Join-Path $PSScriptRoot "media_$($j.s)\videos\$($j.f)\$tag\$($j.s).mp4"
    if (-not ((Test-Path $mp4) -and ($procs[$j.s].ExitCode -eq 0))) { $bad += $j.s }
}
if ($bad.Count -gt 0) {
    Write-Host ""
    Write-Host "Fallaron: $($bad -join ', ')" -ForegroundColor Red
    Write-Host "Mira logs\<escena>.err.txt (copiame el final y lo arreglo)." -ForegroundColor Red
    Write-Host "Para repetir solo esas:  powershell -File render_all.ps1 -Mode $Mode -Only $($bad -join ',')" -ForegroundColor Yellow
}

foreach ($v in $sel) {
    $files = @(); $missing = @()
    foreach ($s in $videos[$v].scenes) {
        $mp4 = Join-Path $PSScriptRoot "media_$s\videos\$($videos[$v].file)\$tag\$s.mp4"
        if (Test-Path $mp4) { $files += $mp4 } else { $missing += $s }
    }
    if ($missing.Count -gt 0) { Write-Host "Video $v incompleto (faltan: $($missing -join ', ')); no lo uno todavia." -ForegroundColor Yellow; continue }
    $listPath = Join-Path $PSScriptRoot "concat_$v.txt"
    $files | ForEach-Object { "file '" + ($_ -replace '\\','/') + "'" } | Set-Content -Path $listPath -Encoding ASCII
    $out = "$($videos[$v].out)_$Mode.mp4"
    ffmpeg -y -loglevel error -f concat -safe 0 -i $listPath -c copy $out
    if ($LASTEXITCODE -eq 0) { Write-Host "LISTO  $out" -ForegroundColor Green } else { Write-Host "ffmpeg fallo uniendo el video $v" -ForegroundColor Red }
}
$min = [int]((Get-Date) - $start).TotalMinutes
Write-Host ""
Write-Host "Terminado en $min min." -ForegroundColor Cyan
