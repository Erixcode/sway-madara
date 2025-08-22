# Amber Red Uchiha Madara theme prompt
PS1='\[\e[1;31m\]\u@\[\e[1;33m\]\h \[\e[1;38;5;166m\]\w \[\e[1;31m\]\$ \[\e[0m\]'

# Alternative with more red emphasis:
# PS1='\[\e[1;38;5;160m\]\u\[\e[0m\]@\[\e[1;38;5;166m\]\h \[\e[1;38;5;172m\]\w \[\e[1;38;5;160m\]\$ \[\e[0m\]'

# For a simpler version:
# PS1='\[\e[1;31m\]\u@\[\e[1;33m\]\h \[\e[1;31m\]\w \$ \[\e[0m\]'
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]; then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH
EDITOR=/usr/bin/vim
# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
    for rc in ~/.bashrc.d/*; do
        if [ -f "$rc" ]; then
            . "$rc"
        fi
    done
fi
unset rc
export GEMINI_API_KEY="OOPS"
export GOOGLE_CLOUD_PROJECT="OOPS"
export FZF_DEFAULT_COMMAND="fd --type f"
export FZF_DEFAULT_OPTS="--style full --preview 'bat --color=always {}' --bind 'focus:transform-header:file --brief {}' --walker-skip .wine"
# export FZF_DEFAULT_OPTS="---style full --preview 'bat --color=always {}'"
source /usr/share/fzf/shell/key-bindings.bash
# highlight Cat
alias cats='highlight -O ansi --force'
