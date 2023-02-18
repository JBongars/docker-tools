function build-and-tag-image {
  param(
    [string]$imageName,
    [string]$version
  )

  $dockerfilePath = Join-Path $scriptPath "images\Dockerfile.${imageName}"
  $localTagName = "dtools_${imageName}:latest"
  $tagName = "julien23/dtools_${imageName}:${version}"
  $latestTagName = "julien23/dtools_${imageName}:latest"
  $noCacheFlag = if ($noCache) { "--no-cache" } else { "" }

  Invoke-Expression "docker build -f ${dockerfilePath} -t ${localTagName} ${noCacheFlag} .."
  docker tag $localTagName $tagName
  docker tag $localTagName $latestTagName
}

$noCache = $args.Contains("--no-cache")
$scriptPath = Split-Path -Parent (Split-Path -Parent (Resolve-Path $MyInvocation.MyCommand.Path))
$packageJsonPath = Join-Path $scriptPath "package.json"

$version = (Get-Content -Path ${packageJsonPath} -Raw | ConvertFrom-Json)."version"
$repo_name = (Get-Content -Path ${packageJsonPath} -Raw | ConvertFrom-Json)."docker_repository"


# Call the function for each Docker image to build and tag
build-and-tag-image "ubuntu" $version $repo_name
build-and-tag-image "docker" $version $repo_name
build-and-tag-image "kube" $version $repo_name
build-and-tag-image "aws" $version $repo_name
build-and-tag-image "awskube" $version $repo_name