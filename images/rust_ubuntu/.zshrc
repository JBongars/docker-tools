export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
source $ZSH/oh-my-zsh.sh

cap () { tee /tmp/capture.out; }
ret () { cat /tmp/capture.out; }

if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi

if [ -f ~/onload.sh ]; then
  . ~/onload.sh
fi

force_execute(){
  if [ -z "$1" ]; then
    echo "Usage: force_execute <command>"
    return 1
  fi
  local command="$1"
  shift
  local args="$@"
  
  if [ -f $command ]; then
    dos2unix $command
  fi
  chmod +x $command

  $command $args
}
alias f="force_execute"

do_until_sucess(){
  if [ -z "$1" ]; then
    echo "Usage: do_until_sucess <command>"
    return 1
  fi
  local command="$@"
  local retries=0

  while true; do
    $command
    if [ $? -eq 0 ]; then
      break
    fi
    retries=$((retries+1))
    echo "Retrying $command... ($retries)"
  done
}
alias dus="do_until_sucess"

alias gb="
  git for-each-ref \
    --sort='-committerdate:iso8601' \
    --format='%(committerdate:relative)|%(refname:short)|%(committername)' \
    refs/heads/ | column -s '|' -t"

alias gbh="
  git for-each-ref \
    --sort='-committerdate:iso8601' \
    --format='%(committerdate:relative)|%(refname:short)|%(committername)' \
    refs/remotes/ | column -s '|' -t"
