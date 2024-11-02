#!/bin/bash
## Note: configured for Debian-based distributions. Other distros will need to use appropriate package managers, etc.

## .bashrc
cp .bashrc ~/.bashrc && source ~/.bashrc

## Install nerd font
if [ ! -d ~/.local/share/fonts/MartianMono ]; then
    wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/MartianMono.zip && unzip MartianMono.zip -d ~/.local/share/fonts && fc-cache -fv
fi

## Install packages
# qtile
if [ ! -d ~/.local/bin/qtile ]; then
    sudo apt install xserver-xorg xinit libpangocairo-1.0-0 python3-pip python3-xcffib python3-cairocffi pipx libiw-dev
    pipx install qtile
    pipx inject qtile qtile-extras psutil iwlib
    cp qtile/qtile.desktop /usr/share/xsessions
fi

# picom
if [ ! -f /usr/local/bin/picom ] && [ ! -f /usr/bin/picom ]; then
    sudo apt install picom
fi

# wezterm
if [ ! -f /usr/share/keyrings/wezterm-fury.gpg ]; then
    curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
    echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
    sudo apt update && sudo apt install wezterm
fi

# nvim
if [ ! -d /opt/nvim-linux64 ] && [ ! -d /opt/nvim ]; then
    curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux64.tar.gz
    sudo rm -rf /opt/nvim
    sudo tar -C /opt -xzf nvim-linux64.tar.gz
    echo "export PATH=/opt/nvim/bin:$PATH" >> ~/.bashrc
fi

chmod +x qtile/autostart_once.sh

## Move config files
mkdir -p ~/.config
chmod +x copy-config.sh
./copy-config.sh
