#!/bin/bash
## Note: this is configured for Debian based distributions. Other distros will need to use appropriate package managers, etc.

## Install packages
# qtile
sudo apt install xserver-xorg xinit libpangocairo-1.0-0 python3-pip python3-xcffib python3-cairocffi
pip install qtile

# nvim
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux64.tar.gz
sudo rm -rf /opt/nvim
sudo tar -C /opt -xzf nvim-linux64.tar.gz
echo "export PATH=/opt/nvim/bin:$PATH" >> ~/.bashrc

# wezterm
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list

sudo apt update && sudo apt install wezterm picom

## Move config files
mkdir -p ~/.config
cp -r wezterm ~/.config/wezterm 
cp -r qtile ~/.config
cp -r nvim ~/.config
cp -r picom ~/.config
