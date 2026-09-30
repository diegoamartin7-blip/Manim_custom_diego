# ======================================================================
#  GAL 1 - PRIMER PARCIAL - 2 videos en un solo batch
#    Video 1: Teoria visual   (complejos, sistemas, matrices, inversa, rango, determinantes)
#    Video 2: Ejercicios      (un ejercicio real de parcial por tipo, de mayor a menor probabilidad)
#
#  Uso:   render_4k.bat   /   render_preview.bat
#         powershell -File render_all.ps1 -Mode 4k|1080|preview
#                    [-Video all|1|2] [-MaxParallel N] [-Only V1_05_Matrices,V2_03_Rango] [-TimeoutMin 240]
#
#  - La lista de escenas se lee del SCENE_ORDER de cada archivo .py.
#  - Todas las escenas corren EN PARALELO, cada una con su carpeta media_<escena>.
#  - Al final, ffmpeg une cada video por separado.
#  - Con -Only re-renderizas solo las que fallaron y se re-unen los videos.
#  - Ritmo: G1_PACE=1.2 (mas lento) o G1_WPS=3.8 (lectura mas lenta) antes de correr.
# ======================================================================
param(
    [ValidateSet("4k", "1080", "preview")][string]$Mode = "4k",
    [ValidateSet("all", "1", "2")][string]$Video = "all",
    [int]$MaxParallel = 0,
    [string[]]$Only = @(),
    [int]$TimeoutMin = 0
)
Set-Location $PSScriptRoot
$ErrorActionPreference = "Continue"
# MaxParallel 0 = automatico, limitado por CPU Y por RAM libre: en 4K cada escena puede
# llegar a ~6 GB (Cairo + ffmpeg + LaTeX). Con 22 escenas a la vez Windows se quedo sin
# memoria virtual ("archivo de paginacion demasiado pequeno"), asi que ahora se regula solo.
$perSceneGB = if ($Mode -eq "4k") { 6 } elseif ($Mode -eq "1080") { 2.5 } else { 1 }
$freeRamGB = 16
try { $freeRamGB = [math]::Floor((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB) } catch { }
if ($MaxParallel -le 0) {
    $byRam = [math]::Max(2, [math]::Floor(($freeRamGB - 6) / $perSceneGB))
    $MaxParallel = [math]::Min([Environment]::ProcessorCount, $byRam)
}
# Vigilante: una escena que pasa este limite se corta (y se avisa), asi el resto no queda esperando toda la noche.
if ($TimeoutMin -le 0) { $TimeoutMin = if ($Mode -eq "4k") { 240 } elseif ($Mode -eq "1080") { 90 } else { 30 } }
# Con "powershell -File", "-Only A,B" llega como un solo texto: lo separo a mano.
$Only = @($Only | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })

function Get-SceneOrder($file) {
    $src = Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot "$file.py")
    $m = [regex]::Match($src, 'SCENE_ORDER\s*=\s*\[(.*?)\]', 'Singleline')
    if (-not $m.Success) { Write-Host "No encontre SCENE_ORDER en $file.py" -ForegroundColor Red; exit 1 }
    return @([regex]::Matches($m.Groups[1].Value, '"([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
}

$videos = [ordered]@{
    "1" = @{ file = "v1_teoria";  out = "GAL1_V1_Teoria_Aplicada" }
    "2" = @{ file = "v2_parcial"; out = "GAL1_V2_Ejercicios_Parcial" }
}
foreach ($k in @($videos.Keys)) { $videos[$k].scenes = Get-SceneOrder $videos[$k].file }
$sel = if ($Video -eq "all") { @("1","2") } else { @($Video) }

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
Write-Host "Manim: $exe $($pre -join ' ')  |  Modo: $Mode ($tag)  |  Escenas: $($jobs.Count)  |  Paralelo: $MaxParallel (RAM libre: $freeRamGB GB)  |  Disco libre: $freeGB GB" -ForegroundColor Cyan

$logDir = Join-Path $PSScriptRoot "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$start = Get-Date

function Clean-Partials($s) {
    $pm = Join-Path $PSScriptRoot "media_$s\videos"
    if (Test-Path $pm) {
        Get-ChildItem $pm -Recurse -Directory -Filter "partial_movie_files" -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ---------- 4) Lanzar en paralelo y esperar (cortando escenas colgadas) ----------
function Run-Batch($list, $par) {
    $script:procs = @{}
    $script:cleaned = @{}
    foreach ($j in $list) {
        while ((@($script:procs.Values | Where-Object { -not $_.HasExited })).Count -ge $par) {
            foreach ($k in @($script:procs.Keys)) { if ($script:procs[$k].HasExited -and -not $script:cleaned[$k]) { Clean-Partials $k; $script:cleaned[$k] = $true } }
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
        # Prioridad baja: la PC sigue usable mientras renderiza.
        try { $p.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal } catch { }
        $script:procs[$s] = $p
        Write-Host "  lanzada  $s" -ForegroundColor DarkGray
    }
    while ((@($script:procs.Values | Where-Object { -not $_.HasExited })).Count -gt 0) {
        foreach ($k in @($script:procs.Keys)) { if ($script:procs[$k].HasExited -and -not $script:cleaned[$k]) { Clean-Partials $k; $script:cleaned[$k] = $true } }
        foreach ($k in @($script:procs.Keys)) {
            $p = $script:procs[$k]
            if (-not $p.HasExited -and ((Get-Date) - $p.StartTime).TotalMinutes -gt $TimeoutMin) {
                Write-Host "  CORTADA $k (mas de $TimeoutMin min). Mandame logs\$k.err.txt" -ForegroundColor Red
                & taskkill /T /F /PID $p.Id *> $null
            }
        }
        $done = (@($script:procs.Values | Where-Object { $_.HasExited })).Count
        $min = [int]((Get-Date) - $start).TotalMinutes
        $running = @($script:procs.Keys | Where-Object { -not $script:procs[$_].HasExited })
        $show = if ($running.Count -le 6) { "  corriendo: " + ($running -join ", ") } else { "" }
        Write-Host ("  {0}/{1} escenas listas  ({2} min){3}" -f $done, $list.Count, $min, $show)
        Start-Sleep -Seconds 20
    }
    foreach ($k in @($script:procs.Keys)) { if (-not $script:cleaned[$k]) { Clean-Partials $k } }
    $failed = @()
    foreach ($j in $list) {
        $mp4 = Join-Path $PSScriptRoot "media_$($j.s)\videos\$($j.f)\$tag\$($j.s).mp4"
        if (-not ((Test-Path $mp4) -and ($script:procs[$j.s].ExitCode -eq 0))) { $failed += $j }
    }
    return ,$failed
}

$failed = Run-Batch $jobs $MaxParallel
# Reintento automatico (casi siempre fue falta de memoria): de a pocas escenas.
if ($failed.Count -gt 0) {
    $retryPar = [math]::Min(3, $MaxParallel)
    Write-Host ""
    Write-Host "Reintentando $($failed.Count) escena(s) de a $retryPar : $(($failed | ForEach-Object { $_.s }) -join ', ')" -ForegroundColor Yellow
    $failed = Run-Batch $failed $retryPar
}

# ---------- 6) Verificar y unir cada video ----------
$bad = @($failed | ForEach-Object { $_.s })
if ($bad.Count -gt 0) {
    Write-Host ""
    Write-Host "Fallaron (tambien en el reintento): $($bad -join ', ')" -ForegroundColor Red
    Write-Host "Mira logs\<escena>.err.txt (copiame el final y lo arreglo)." -ForegroundColor Red
    Write-Host "Para repetir solo esas:  powershell -File render_all.ps1 -Mode $Mode -Only $($bad -join ',') -MaxParallel 2" -ForegroundColor Yellow
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
