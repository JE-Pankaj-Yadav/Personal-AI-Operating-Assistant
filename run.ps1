$ErrorActionPreference='Stop'
$ROOT=(Resolve-Path (Join-Path $PSScriptRoot '.')).Path
Write-Host "PA NEXUS root: $ROOT"
$py=Get-Command python -ErrorAction SilentlyContinue
if(-not $py){throw 'Python 3.11-3.14 is required.'}
$pv=& $py.Source --version 2>&1
if($pv -notmatch 'Python 3\.(11|12|13|14)'){throw "Unsupported Python: $pv"}
$node=Get-Command node -ErrorAction SilentlyContinue
if(-not $node){throw 'Node 20-22 is required; install a supported Node runtime.'}
$nv=& $node.Source --version
if($nv -notmatch '^v(20|21|22)\.') {throw "Unsupported Node: $nv. Use Node 20-22."}
$venvPy="$ROOT\.venv\Scripts\python.exe"
if(Test-Path $venvPy){
  $venvPv=& $venvPy --version 2>&1
  if($venvPv -notmatch ('Python '+[regex]::Escape(($pv -replace '^Python ','')))){
    Write-Host "Existing virtual environment uses $venvPv; recreating it for $pv."
    Remove-Item -Recurse -Force "$ROOT\.venv"
  }
}
if(-not(Test-Path $venvPy)){& $py.Source -m venv "$ROOT\.venv"}
& $venvPy -m pip install --upgrade pip
& $venvPy -m pip install -r "$ROOT\backend\requirements.txt"
Push-Location "$ROOT\backend"; try { $env:PYTHONPATH='.'; & $venvPy -m alembic upgrade head; & $venvPy -c 'import app.main' } finally { Pop-Location }
Push-Location "$ROOT\frontend"; try { $npm=(Get-Command npm -ErrorAction SilentlyContinue).Source; if(-not $npm){throw 'npm not found'}; if(Test-Path package-lock.json){& $npm ci}else{Write-Warning 'package-lock.json is missing; run npm install once to generate it.'; & $npm install}; & $npm run typecheck; & $npm run build } finally { Pop-Location }
if(-not(Test-Path "$ROOT\frontend\dist\index.html")){throw 'Frontend build missing dist/index.html'}
$env:PYTHONPATH="$ROOT\backend"; & $venvPy -m uvicorn app.main:app --host 127.0.0.1 --port 8011
