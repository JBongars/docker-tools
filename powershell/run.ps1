function ubuntu {
  $argsString = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work $argsString ubuntu:latest bash"
}

function dubuntu {
  $argsString = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work ${argsString} julien23/dtools_ubuntu:latest zsh"
}

function kube {
  $argsString = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -ti -v ${PWD}:/work  -v //var/run/docker.sock:/var/run/docker.sock ${argsString} julien23/dtools_kube:latest zsh"
}

function aws {
  $argsString = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -it -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws ${argsString} julien23/dtools_aws:latest zsh"
}

function awskube {
  $argsString = $args.Count -eq 0 ? '' : $args[0] | ForEach-Object { "$_" }
  Invoke-Expression "docker run -it -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws -v //var/run/docker.sock:/var/run/docker.sock ${argsString} julien23/dtools_awskube:latest zsh"
}

$repo_name = npm view $(Join-Path $PSScriptRoot "..") docker_repository
$remainingArgsString

if ($args.Count -eq 0) {
    Write-Output "Please specify a function to call as an argument."
} else {
    $functionName = $args[0]

    if (Get-Command $functionName -ErrorAction SilentlyContinue) {
        $remainingArgs = $args.Count -gt 1 ? $args[1..($args.Count - 1)] -join ' ' : ''
        & $functionName $remainingArgs
    } else {
        Write-Output "Function '$functionName' not found."
    }
}