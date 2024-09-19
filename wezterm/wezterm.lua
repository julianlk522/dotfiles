-- Pull in the wezterm API
local wezterm = require("wezterm")

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme = "Cobalt Neon (Gogh)"

config.font = wezterm.font("SpaceMono Nerd Font")
config.font_size = 10.0
config.inactive_pane_hsb = {
	saturation = 0.9,
	brightness = 0.8,
}
config.window_background_image = "~/.config/wezterm/bg.jpg"
config.window_background_image_hsb = {
	brightness = 0.02,
	hue = 1.0,
	saturation = 0.1,
}
config.window_background_opacity = 0.9

config.initial_rows = 35
config.initial_cols = 150

-- and finally, return the configuration to wezterm
return config
