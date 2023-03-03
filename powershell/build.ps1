param (
    [string]$name = ""
)

function build-and-tag-image {
  param(
    [string]$imageName,
    [string]$version
  )

  $dockerfilePath = Join-Path $scriptPath "images\Dockerfile.${imageName}"
  $localTagName = "dtools_${imageName}:latest"
  $tagName = "julien23/dtools_${imageName}:${version}"
  $latestTagName = "julien23/dtools_${imageName}:latest"
  
  Write-Output "docker build -f ${dockerfilePath} -t ${localTagName} ${buildArgs} .."

  Invoke-Expression "docker build -f ${dockerfilePath} -t ${localTagName} ${buildArgs} .."
  docker tag $localTagName $tagName
  docker tag $localTagName $latestTagName
}

$scriptPath = Split-Path -Parent (Split-Path -Parent (Resolve-Path $MyInvocation.MyCommand.Path))
$packageJsonPath = Join-Path $scriptPath "package.json"

$version = (Get-Content -Path ${packageJsonPath} -Raw | ConvertFrom-Json)."version"
$repo_name = (Get-Content -Path ${packageJsonPath} -Raw | ConvertFrom-Json)."docker_repository"
$buildArgs = $args.Count -gt 0 ? $args[0..($args.Count - 1)] -join ' ' : ''


if ($name -ne "") {
  build-and-tag-image $name $version $repo_name
} else {
  # Call the function for each Docker image to build and tag
  build-and-tag-image "alpine_base" $version $repo_name
  build-and-tag-image "alpine_dind_base" $version $repo_name
  build-and-tag-image "ubuntu" $version $repo_name
  build-and-tag-image "golang" $version $repo_name
  build-and-tag-image "kube" $version $repo_name
  build-and-tag-image "aws" $version $repo_name
  build-and-tag-image "awskube" $version $repo_name
  build-and-tag-image "github_actions" $version $repo_name
}