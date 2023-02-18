function ubuntu {
  docker run -ti -v "${PWD}:/work" ubuntu bash
}

function dubuntu {
  docker run -ti -v "${PWD}:/work" julien23/dtools_ubuntu:latest zsh
}

function kube {
  docker run -ti -v "${PWD}:/work"  -v //var/run/docker.sock:/var/run/docker.sock julien23/dtools_kube:latest zsh
}

function aws {
  docker run -it -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws julien23/dtools_aws:latest zsh
}

function awskube {
  docker run -it -v ${PWD}:/work -v $env:USERPROFILE\.aws:/root/.aws -v //var/run/docker.sock:/var/run/docker.sock julien23/dtools_awskube:latest zsh
}

$repo_name = npm view $(Join-Path $PSScriptRoot "..") docker_repository

if ($args.Count -eq 0) {
    Write-Output "Please specify a function to call as an argument."
} else {
    $functionName = $args[0]

    if (Get-Command $functionName -ErrorAction SilentlyContinue) {
        $remainingArgs = $args[1..($args.Count - 1)]
        & $functionName $remainingArgs
    } else {
        Write-Output "Function '$functionName' not found."
    }
}