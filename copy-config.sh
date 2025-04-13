#!/usr/bin/env bash

directories=(
    "qtile" 
    "picom" 
    "wezterm" 
    "nvim"
)

for dir in "${directories[@]}"
do
    cp -r "$dir" ~/.config
    echo "Copied $dir to ~/.config"
done

files=(
    ".bashrc"
    ".inputrc"
    ".gitconfig"
)

for file in "${files[@]}"
do
    cp "$file" ~
    echo "Copied $file to ~"
done
