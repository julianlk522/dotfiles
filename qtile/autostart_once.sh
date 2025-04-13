#!/usr/bin/env bash

picom -b --config ~/.config/picom/picom.conf &
firefox &
wezterm &
wezterm start --cwd ~/Documents/obsidian
