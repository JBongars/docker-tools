export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

cap () { tee /tmp/capture.out; }
ret () { cat /tmp/capture.out; }

if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi

source $ZSH/oh-my-zsh.sh
