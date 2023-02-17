New-Alias -Name d -Value docker

Set-Alias -Name dubuntu -Value { d run -ti -p 80:80 -v "${PWD}:/work" ubuntu bash }
