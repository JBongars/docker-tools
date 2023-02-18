# $randomNumber = Get-Random -Minimum 3000 -Maximum 9001

function ubuntu {
  docker run -ti -p 80:80 -v "${PWD}:/work" ubuntu bash
}

function dubuntu {
  docker run -ti -p 80:80 -v "${PWD}:/work" dtools_ubuntu:latest zsh
}

function kube {
  docker run -ti -p 80:80 -v "${PWD}:/work" dtools_kube:latest zsh
}


# Check if the script was called with an argument
if ($args.Count -eq 0) {
    Write-Output "Please specify a function to call as an argument."
} else {
    # Get the name of the function to call from the first argument
    $functionName = $args[0]

    # Check if the function exists
    if (Get-Command $functionName -ErrorAction SilentlyContinue) {
        # Call the function with the remaining arguments
        $remainingArgs = $args[1..($args.Count - 1)]
        & $functionName $remainingArgs
    } else {
        Write-Output "Function '$functionName' not found."
    }
}