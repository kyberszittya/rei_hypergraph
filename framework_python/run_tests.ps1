$folder = './output/'
if (-not (Test-Path -Path $folder)) {
    Create-Item $folder -ItemType Directory
    Write-Host "Created folder [$folder]"
}
pytest ./test/
#pytest --cov=src test/