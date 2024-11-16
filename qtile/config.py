from os.path import expanduser
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


@hook.subscribe.startup_once
def startup_once():
    subprocess.Popen(expanduser("~/.config/qtile/autostart_once.sh"))

MOD = "mod4"
TERMINAL = "wezterm"

keys = [

    # Switch windows
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([MOD], "w", lazy.window.kill(), desc="Kill focused window"),
    KeyChord([MOD], "z", [
        Key([], "h", lazy.prev_screen(), desc="Move to previous screen"),
        Key([], "l", lazy.next_screen(), desc="Move to next screen"),
    ]),

    # Move windows
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),


    # Grow windows
    Key([MOD, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Switch layouts
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [MOD],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([MOD], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    # Toggle split / unsplit stack modes
    Key(
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Run Commands
    Key([MOD], "Return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Open web browser
    Key([MOD], "b", lazy.spawn("firefox"), desc="Open web browser"),

    # Increase / decrease brightness (LAPTOP ONLY)
    # Key([], "F3", lazy.spawn("brightnessctl s +5%"), desc="Increase display brightness"),
    # Key([], "F2", lazy.spawn("brightnessctl s 5%-"), desc="Decrease display brightness"),

    # Reset / shutdown qtile
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
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
                [MOD],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [MOD, "shift"],
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

active_network_interface = None
try:
    active_network_interface = subprocess.check_output(["ip", "route", "show", "default"]).decode("utf-8").split("dev ")[1].split(" ")[0]
except (subprocess.CalledProcessError, IndexError):
    pass

SPACER_LENGTH = 8
BORDER_WIDTH = [0, 0, 2, 0]
BAR_SIZE = 24

# Define widgets list as a function so Wlan can be conditionally added
# if active_network_interface can be determined
def get_top_bar_widgets():
    widgets = [
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
        widget.Spacer(SPACER_LENGTH),
        widget.CPU(
             format = '▓  CPU: {load_percent}%',
             foreground = colors[4],
             decorations=[
                 BorderDecoration(
                     colour = colors[4],
                    border_width = BORDER_WIDTH,
                 )
             ],
         ),
        widget.Spacer(SPACER_LENGTH),
        widget.Memory(
            foreground = colors[4],
            mouse_callbacks = {'Button1': lambda: qtile.spawn(TERMINAL + ' -e htop')},
                 format = '{MemUsed: .0f}{mm}',
            fmt = '🖥  Mem: {} used',
            decorations=[
                BorderDecoration(
                    colour = colors[4],
                    border_width = BORDER_WIDTH,
                 )
            ],
         ),
        widget.Spacer(SPACER_LENGTH),
    ]

    if active_network_interface is not None:
        widgets.extend([
            widget.Wlan(
                interface = active_network_interface,
                foreground = colors[5],
                format = '📶  {essid} {quality}/70',
                decorations=[
                    BorderDecoration(
                        colour = colors[5],
                        border_width = BORDER_WIDTH,
                    )
                ]
            ),
            widget.Spacer(SPACER_LENGTH),
        ])

    widgets.extend([
        widget.Net(
            foreground = colors[5],
            format = '📡 {down:6.2f}{down_suffix:<2}↓↑{up:6.2f}{up_suffix:<2}',
            decorations=[
                BorderDecoration(
                    colour = colors[5],
                    border_width = BORDER_WIDTH,
                )
            ],
        ),
        widget.Spacer(SPACER_LENGTH),
        widget.OpenWeather(
            cityid = '4459467', # replace with desired city ID (https://openweathermap.org/find)
            metric = False,
            format = '{location_city}: {main_temp}°F - {humidity}% hum. - {weather_details}',
            foreground = colors[3],
            decorations=[
                BorderDecoration(
                    colour = colors[3],
                    border_width = BORDER_WIDTH,
                )
            ],
        ),
        widget.Spacer(SPACER_LENGTH),
        widget.Clock(
            foreground = colors[6],
            format = "⏱  %Y-%m-%d %a %I:%M %p",
            decorations=[
                BorderDecoration(
                    colour = colors[6],
                    border_width = BORDER_WIDTH,
                )
            ],
         ),
        widget.Systray(padding = 3),
        widget.Spacer(SPACER_LENGTH),
    ])
    
    return widgets

screens = [
    Screen(
        top=bar.Bar(
            get_top_bar_widgets(),
            BAR_SIZE,
        ),
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.Spacer(SPACER_LENGTH),
                widget.Prompt(),
                widget.WindowName(foreground=colors[4], max_chars=100),
                widget.Spacer(SPACER_LENGTH),
                widget.QuickExit(default_text='[ Off ]', countdown_format='[ {} ]   ', foreground=colors[8]),
            ],
            BAR_SIZE
        ),
        wallpaper="~/.config/qtile/wallpaper/bg.jpg",
        wallpaper_mode='fill',
    ),
]

# Floating layout
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

# Configs
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
