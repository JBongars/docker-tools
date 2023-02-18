
$repo_name = npm view $(Join-Path $PSScriptRoot "..") docker_repository
$images = docker images --filter "reference=${repo_name}/dtools_*" --format "{{.Repository}}:{{.Tag}}"

$images | ForEach-Object -Parallel {
  $image = $_
  Write-Host "$image is pushing..."
  docker push $image > $null
  Write-Host "`r${image} done"
}