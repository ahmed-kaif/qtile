
##########################
# title: qtile           #
# tags: config.py        #
# author: thelinuxfraud  #
##########################

import os
import re
import socket
import subprocess
from typing import List
from libqtile import layout, bar, widget, hook, qtile, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration

if qtile.core.name == "x11":
    term = "alacritty"
elif qtile.core.name == "wayland":
    term = "alacritty"

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')
myTerm = "alacritty"
myBrowser = "firefox"


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function#
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# The Essentials
    Key([mod], "r", lazy.spawncmd(), desc="Spawn prompt widget"),
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Web browser"),
    Key([mod, "shift"], "Return", lazy.spawn("thunar"), desc="File manager"),
    Key([mod, "shift"], "d", lazy.spawn("rofi -show drun"), desc="App launcher"),
    Key([mod, "shift"], "e", lazy.spawn("emacs"), desc="Doom Emacs"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "s", lazy.run_extension(extension.CommandSet(
            commands = {
            "reboot": "reboot",
            "shutdown" : "shutdown",
            },
            dmenu_lines = 2
    ))),
# Functions
    Key([mod], "m", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),

# Change Layouts 
    Key([mod], "space", lazy.next_layout(), desc="Change layout"),

# Change Window Focus
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),

# Resize Windows
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
#group_labels = ["web", "dev", "sys", "doc", "file", "vbox", "edit", "photos", "vid", "gfx",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "control"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":10,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#2E3440"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme, new_client_position='top'),
    layout.Max()
]

# COLORS FOR THE BAR
def init_colors():
    return [["#D8DEE9", "#D8DEE9"], # color 0
            ["#2E3440", "#2E3440"], # color 1
            ["#4C566A", "#4C566A"], # color 2
            ["#A3BE8C", "#A3BE8C"], # color 3
            ["#EBCB8B", "#EBCB8B"], # color 4
            ["#5E81AC", "#5E81AC"], # color 5
            ["#BF616A", "#BF616A"], # color 6
            ["#81A1C1", "#81A1C1"], # color 7
            ["#D08770", "#D08770"], # color 8
            ["#88C0D0", "#88C0D0"]] # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

myFont = "CaskaydiaCove Nerd Font"
myFontBold = "CaskaydiaCove Nerd Font Bold"

def init_widgets_defaults():
    return dict(font=myFont,
                fontsize = 15,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CurrentLayoutIcon(
                        padding = 4,
                        scale = 0.6,
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.GroupBox(
                        font= myFont,
                        fontsize = 15,
                        margin_y = 2,
                        margin_x = 3,
                        padding_y = 2,
                        padding_x = 3,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[3],
                        inactive = colors[0],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[4],
                        foreground = colors[0],
                        background = colors[1],
                        # decorations = [
                        #     RectDecoration (
                        #         colour = colors[3],
                        #         padding_y = 3,
                        #         radius = 2,
                        #         filled = True
                        #     ),
                        # ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2],
                        ),
               widget.WindowName(
                        font=myFontBold,
                        fontsize = 15,
                        foreground = colors[0],
                        background = colors[1],
                        #decorations = [
                        #    RectDecoration (
                        #        colour = colors[5],
                        #        padding_y = 5,
                        #        radius = 2,
                        #        filled = True
                        #    ),
                        #    ],
                            ),
               widget.Sep(
                        foreground = colors[2],
                        background = colors[1],
                        padding = 5,
                        linewidth = 1
                        ),
               widget.Net(
                        foreground = colors[1],
                        background = colors[1],
                        font = myFontBold,
                        fontsize = 15,
                        format = '{down} ↓↑ {up}',
                        interface = 'wlp1s0',
                        decorations = [
                            RectDecoration (
                                colour = colors[4],
                                padding_y = 3,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CPU(
                        background = colors[1],
                        foreground = colors[1],
                        font = myFontBold,
                        fontsize = 15,
                        decorations = [
                            RectDecoration (
                                colour = colors[3],
                                padding_y = 3,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.Memory(
                        measure_mem = 'G',
                        foreground = colors[1],
                        background = colors[1],
                        font = myFontBold,
                        fontsize = 15,
                        decorations = [
                            RectDecoration (
                                colour = colors[6],
                                padding_y = 3,
                                radius = 2,
                                filled = True
                                ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.DF(
                        visible_on_warn = False,
                        background = colors[1],
                        foreground = colors[1],
                        font = myFontBold,
                        fontsize = 15,
                        decorations = [
                            RectDecoration (
                                colour = colors[7],
                                padding_y = 3,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2]
                        ),
               widget.Clock(
                        foreground = colors[1],
                        background = colors[1],
                        font = myFontBold,
                        fontsize = 15,
                        format = "%a %d %b %H:%M",
                        decorations = [
                            RectDecoration (
                                colour = colors[8],
                                padding_y = 3,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.UPowerWidget(
                        battery_height = 12,
                        battery_width = 24,
                        border_colour = '#d8dee9',
                        border_critical_colour = '#bf616a',
                        border_charge_colour = '#81a1c1',
                        fill_charge = '#a3be8c',
                        fill_low = '#ebcb8b',
                        fill_critical = '#bf616a',
                        fill_normal = '#d8dee9',
                        percentage_low = 0.4,
                        percentage_critical = 0.2,
                        font = myFontBold
                        ),
                widget.Systray(
                        background = colors[1],
                        icon_size = 20,
                        padding = 3
                ),
                widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1] 
                        ),
                widget.Pomodoro(
                        font = myFontBold,
                        fontsize = 15,
                        foreground = colors[1],
                        length_pomodoroi = 25,
                        color_inactive = colors[1],
                        color_active = colors[1],
                        decorations = [
                            RectDecoration (
                                colour = colors[3],
                                padding_y = 3,
                                radius = 2,
                                filled = True
                            ),
                        ],
                ),
                # widget.OpenWeather(
                #         app_key = "4cf3731a25d1d1f4e4a00207afd451a2",
                #         cityid = "4997193",
                #         format = '{main_temp}° {icon}',
                #         metric = False,
                #         font = myFontBold,
                #         fontsize = 15,
                #         background = colors[1],
                #         foreground = colors[0],
                #         decorations = [
                #             RectDecoration (
                #                 colour = colors[1],
                #                 padding_y = 5,
                #                 radius = 2,
                #                 filled = True 
                #             ),
                #         ],
                #         ),
                widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2]
                        ),
                widget.Prompt(
                        font = myFontBold,
                        fontsize = 15
                ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


widgets_screen1 = init_widgets_screen1()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, opacity=1.0))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []


main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),

], fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"

