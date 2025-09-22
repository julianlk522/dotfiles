#
# ~/.bashrc
#

# don't put duplicate lines or lines starting with space in the history.
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

HISTSIZE=1000
HISTFILESIZE=2000

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1_CMD1=''
PS1='\[\e[96m\][\T]\[\e[0m\] \[\e[92;1m\]\u@\h:\[\e[0;96m\]\w${PS1_CMD1}\[\e[92;1m\]\$\[\e[0m\] '

alias ls='ls -AhX --color=auto --group-directories-first'
alias ll='ls -alF'
alias l='ls -CF'
alias grep='grep --color=auto'

alias p='sudo pacman'
alias nmrestart='sudo service NetworkManager restart'
alias voff='pactl set-sink-mute @DEFAULT_SINK@ toggle'
alias vup='pactl set-sink-volume @DEFAULT_SINK@ +5%'
alias vdown='pactl set-sink-volume @DEFAULT_SINK@ -5%'
alias vset='pactl set-sink-volume @DEFAULT_SINK@'

alias dotfiles='cd ~/Documents/dotfiles'
alias cdf='copy_to_dotfiles.sh'

code_dir="$HOME/Documents/code"
alias gcd='cd $(find "$code_dir" -type d | fzf)'

# 👽 Modeep
setup_modeep_dev() {
    local modeep_frontend_dir="$code_dir/JS-TS/Astro/modeep-frontend"
    local modeep_backend_dir="$code_dir/Go/modeep-backend"

    code "$modeep_frontend_dir" &
    code "$modeep_backend_dir" &
    
    # wezterm cli spawn --new-window --cwd "$modeep_backend_dir" -- bash -c 'direnv allow && eval "$(direnv export bash)" && ./run.sh; exec bash' &
    kitty @ new-window --cwd "$modeep_backend_dir" bash -c 'direnv allow && eval "$(direnv export bash)" && ./run.sh; exec bash'
    
    cd "$modeep_frontend_dir" && bash -c 'npm run dev; exec bash'
}
alias mddev='setup_modeep_dev'

# 📝 julianlk.com
setup_jlk_dev() {
    local jlk_dotcom_dir="$code_dir/Go/julianlk.com"

    # wezterm cli spawn --new-window --cwd "$jlk_dotcom_dir" -- bash -c 'hugo server -D; exec bash' > /dev/null & disown
    kitty @ new-window --cwd "$jlk_dotcom_dir" bash -c 'hugo server -D; exec bash' > /dev/null & disown
    nvim "$jlk_dotcom_dir"
}
alias jlkdev='setup_jlk_dev'

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# direnv
eval "$(direnv hook bash)"
