export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

plugins=(git)
if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi

source $ZSH/oh-my-zsh.sh
