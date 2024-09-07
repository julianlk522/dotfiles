import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


@hook.subscribe.startup_once
def startup_once():

    subprocess.run('~/.config/qtile/autostart_once.sh')

mod = "mod4"
terminal = guess_terminal()

keys = [

    # Switch windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),


    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),


    # Grow windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Switch layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    # Toggle split / unsplit stack modes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Run Commands
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Open terminal to code
    Key([mod], "c", lazy.spawn(terminal + " --working-directory=/home/julian/Documents/Code"), desc="Open terminal to home/Documents/Code"),

    # Open web browser
    Key([mod], "b", lazy.spawn("firefox"), desc="Open web browser"),

    # Increase / decrease brightness
    Key([], "F3", lazy.spawn("brightnessctl s +5%"), desc="Increase display brightness"),
    Key([], "F2", lazy.spawn("brightnessctl s 5%-"), desc="Decrease display brightness"),

    # Reset / shutdown qtile
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# Groups
group_labels = ["Dev","WWW",]
groups = [Group(
    name=str(group_labels.index(i)+1), label=i) for i in group_labels]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

# Theme
colors  = [
    ["#282a36", "#282a36"], # bg (dark grey)
    ["#f8f8f2", "#f8f8f2"], # fg (yellowish white)
    ["#000000", "#000000"], # black
    ["#ff5555", "#ff5555"], # strawberry
    ["#50fa7b", "#50fa7b"], # green with a hint of blue
    ["#f1fa8c", "#f1fa8c"], # butter
    ["#bd93f9", "#bd93f9"], # violet
    ["#ff79c6", "#ff79c6"], # hot pink
    ["#9aedfe", "#9aedfe"]  # light blue
]

layout_theme = {
    "border_width": 4,
    "margin": 2,
    "border_focus": colors[8],
    "border_normal": colors[0],
}
    
layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
]

# Widgets
widget_defaults = dict(
    font="sans",
    fontsize=20,
    padding=0,
    background=colors[0],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Prompt(foreground=colors[1]),
                widget.GroupBox(
                    fontSize=12,
                    margin_y=5,
                    margin_x=5,
                    padding_y=0,
                    padding_x=1,
                    borderwidth=3,
                    active=colors[8],
                    inactive=colors[1],
                    rounded=False,
                    highlight_color=colors[2],
                    highlight_method="line",
                    this_current_screen_border=colors[7],
                    this_screen_border=colors[4],
                    other_current_screen_border=colors[7],
                    other_screen_border=colors[4],
                ),
                widget.TextBox(
                    text="|",
                    padding=2,
                    foreground=colors[1],
                ),
                widget.Spacer(length = 8),
                widget.CPU(
                     format = '▓  CPU: {load_percent}%',
                     foreground = colors[4],
                     decorations=[
                         BorderDecoration(
                             colour = colors[4],
                            border_width = [0, 0, 2, 0],
                         )
                     ],
                 ),
                widget.Spacer(length = 8),
                widget.Memory(
                    foreground = colors[4],
                    mouse_callbacks = {'Button1': lambda: qtile.spawn(terminal + ' -e htop')},
                         format = '{MemUsed: .0f}{mm}',
                    fmt = '🖥  Mem: {} used',
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                         )
                    ],
                 ),
                widget.Spacer(length = 8),
                widget.Battery(
                    battery = 'CMB0',
                    foreground = colors[4],
                    format = '🔋  Bat: {percent:2.0%}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                        )
                    ]
                ),
                widget.Spacer(),
                widget.Backlight(
                    backlight_name = 'intel_backlight',
                    format = '🔆  Brightness: {percent:2.0%}',
                    foreground = colors[3],
                    decorations=[
                        BorderDecoration(
                            colour = colors[3],
                            border_width = [0, 0, 2, 0],
                        )
                    ],

                ),
                widget.Spacer(length = 8),
                widget.Wlan(
                    interface = 'wlp0s20f3',
                    foreground = colors[5],
                    format = '📶  {essid} {quality}/70',
                    decorations=[
                        BorderDecoration(
                            colour = colors[5],
                            border_width = [0, 0, 2, 0],
                        )
                    ]
                ),
                widget.Spacer(length = 8),
                widget.Net(
                    foreground = colors[5],
                    format = '📡 {down:6.2f}{down_suffix:<2}↓↑{up:6.2f}{up_suffix:<2}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[5],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Clock(
                    foreground = colors[6],
                    format = "⏱  %Y-%m-%d %a %I:%M %p",
                    decorations=[
                        BorderDecoration(
                            colour = colors[6],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                 ),
                widget.Systray(padding = 3),
                widget.Spacer(length = 8),
            ],
            24,
        ),
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.Spacer(length = 8),
                widget.Prompt(),
                widget.WindowName(foreground=colors[4], max_chars=100),
                widget.Spacer(length = 8),
                widget.QuickExit(default_text='[ Off ]', countdown_format='[ {} ]   ', foreground=colors[8]),
            ],
            24,
        ),
        wallpaper="~/.config/qtile/wallpaper/guts.jpg",
        wallpaper_mode='fill',
    ),
]

# Floating layout
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
