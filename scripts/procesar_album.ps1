<#
.SYNOPSIS
  Procesa y numera fotos o copia un PDF dentro de paginas/[ID]/
.EXAMPLE
  .\scripts\procesar_album.ps1 -Id "boda-marcos" -Origen "C:\Fotos"
#>
param(
    [Parameter(Mandatory=$true)][string]$Id,
    [Parameter(Mandatory=$true)][string]$Origen
)

$dest = Join-Path "paginas" $Id
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Force -Path $dest | Out-Null }

if (Test-Path $Origen -PathType Leaf) {
    if ($Origen.EndsWith(".pdf")) {
        Copy-Item $Origen (Join-Path $dest "album.pdf") -Force
        Write-Host "PDF copiado a $dest\album.pdf" -ForegroundColor Green
    }
} elseif (Test-Path $Origen -PathType Container) {
    $fotos = Get-ChildItem $Origen -Include *.jpg,*.jpeg,*.png,*.webp -Recurse | Sort-Object Name
    $i = 1
    foreach ($f in $fotos) {
        $target = Join-Path $dest "$i.jpg"
        Copy-Item $f.FullName $target -Force
        Write-Host "Copiado: $($f.Name) -> $i.jpg" -ForegroundColor Cyan
        $i++
    }
    Write-Host "Total: $($i - 1) fotos numeradas en $dest" -ForegroundColor Green
}