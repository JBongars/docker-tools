param (
  [switch]$dood #docker out of docker
)

function stop_container {
  param (
    [string]$container_id
  )
  Write-Host "Stopping container..."
  Invoke-Expression "docker stop $container_id"

  Write-Host "Removing container..."
  Invoke-Expression "docker rm $container_id"
}

function run_docker_container {
  param (
    [string]$image_name,
    [string]$run_dood_string,
    [string]$run_dind_string,
    [string]$exec_dind_string = "zsh"
  )

  if ($dood){ 
    Invoke-Expression $run_dood_string
  } else {
    Invoke-Expression $run_dind_string

    $cleanup_flag = $true
    $container_id = Invoke-Expression "docker ps -q -f ancestor=${image_name}" | Sort-Object -Descending | Select-Object -First 1
    Invoke-Expression "docker exec -it $container_id $exec_dind_string"

    & stop_container $container_id
    $cleanup_flag = $false

    trap {
      if($cleanup_flag){
        & stop_container $container_id
      }
    } EXIT
  }
}

function ubuntu {
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work --rm $args_string ubuntu:latest bash"
}

function dubuntu {
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work --rm ${args_string} julien23/dtools_ubuntu:latest zsh"
}

function golang {
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work --rm ${args_string} julien23/dtools_golang:latest zsh"
}
  
function kube {
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  $image_name = "julien23/dtools_kube:latest"

  & run_docker_container $image_name `
    "docker run -ti -v ${PWD}:/work  -v //var/run/docker.sock:/var/run/docker.sock --rm ${args_string} $image_name zsh" `
    "docker run -d -v ${PWD}:/work --rm --privileged ${args_string} ${image_name}"
}

function aws {
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -it -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws --rm ${args_string} julien23/dtools_aws:latest zsh"
}

function awskube {
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  $image_name = "julien23/dtools_awskube:latest"

  & run_docker_container $image_name `
  "docker run -it -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws -v //var/run/docker.sock:/var/run/docker.sock --rm ${args_string} ${image_name} zsh"
  "docker run -d -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws --rm --privileged ${args_string} ${image_name}"

  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
}

function github_actions {
  # if ($args.Count -lt 4) {
  #   Write-Output "Usage: de github_actions -e GITHUB_REPO_URL='' -e GITHUB_TOKEN=''"
  #   exit 1
  # }
  $args_string = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work ${args_string} julien23/dtools_github_actions:latest /bin/sh"
}

# $repo_name = npm view $(Join-Path $PSScriptRoot "..") docker_repository
$remaining_args_string

if ($args.Count -eq 0) {
    Write-Output "Please specify a function to call as an argument."
} else {
    $function_name = $args[0]

    if (Get-Command $function_name -ErrorAction SilentlyContinue) {
        $remaining_args = $args.Count -gt 1 ? $args[1..($args.Count - 1)] -join ' ' : ''
        & $function_name $remaining_args
    } else {
        Write-Output "Function '$function_name' not found."
    }
}