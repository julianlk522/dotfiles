#!/bin/bash

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