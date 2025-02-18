local wezterm = require("wezterm")
local config = wezterm.config_builder()

config.color_scheme = "Cobalt Neon (Gogh)"
config.font = wezterm.font("MartianMono Nerd Font")
config.font_size = 10.0

config.inactive_pane_hsb = {
	saturation = 0.9,
	brightness = 0.8,
}
-- config.window_background_image = "~/.config/wezterm/bg.jpg"
config.window_background_image_hsb = {
	brightness = 0.02,
	hue = 1.0,
	saturation = 0.1,
}
config.window_background_opacity = 0.85

config.initial_rows = 35
config.initial_cols = 150

config.keys = {
	{
		key = "q",
		mods = "CTRL",
		action = wezterm.action.CloseCurrentPane({ confirm = false }),
	},
}
return config