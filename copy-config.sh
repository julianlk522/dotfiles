#!/usr/bin/env bash

directories=(
    "hypr"
    "kitty"
    "nvim"
    "picom" 
    "qtile"
    "redshift"
    "waybar"
    "wezterm" 
)

for dir in "${directories[@]}"
do
    cp -r ".config/$dir" ~/.config
    echo "Copied $dir to ~/.config"
done

files=(
    ".bashrc"
    ".bash_profile"
    ".inputrc"
    ".gitconfig"
    ".gitignore"
)

for file in "${files[@]}"
do
    cp "$file" ~
    echo "Copied $file to ~"
done

cp -r bin/* ~/bin
echo "Copied bin to ~/bin"

cp -r Pictures/* ~/Pictures
echo "Copied Pictures to ~/Pictures"

