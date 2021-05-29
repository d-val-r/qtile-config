# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import re
import subprocess as sp

mod = "mod4"
terminal = "alacritty"
browser = "brave"
mail = "thunderbird"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Custom keybindings that I set

    Key([mod], "b", lazy.spawn(browser), desc="Launch default browser"),
    Key([mod, "shift"], "space", lazy.spawn("libreoffice"), desc="Launch LibreOffice"),
    Key([mod, "control"], "u", lazy.spawn("discord"), desc="Launch Discord"),
    Key([mod], "t", lazy.spawn(mail), desc="Launch mail client"),
]

# groups = [Group(i) for i in "123456789"]

groups = [Group(i) for i in ["WEB", "WRITE", "DEV", "FILE", "DISC", "MATH", "DESK", "MAIL"]]
letters = "asdfuiop"
j = 0
for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], letters[j], lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], letters[j], lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])
    j+=1

layouts = [
    # layout.Columns(border_focus_stack='#d75f5f'),
    layout.MonadTall(border_focus='DE781F', border_width=1),
    layout.Max(),
    layout.Floating()
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Ubuntu Bold',
    fontsize=10,
    padding=3,
)
extension_defaults = widget_defaults.copy()



command_output = sp.Popen(['df', '-h'], stdout=sp.PIPE, stderr=sp.STDOUT)
output, error = command_output.communicate()
decoded_output = output.decode().split("\n")

sda_usage = 0
sda_max = 0

sdb_usage = 0
sdb_max = 0

sdc_usage = 0
sdc_max = 0

for line in decoded_output:
    if (re.search("sda3", line)):
        sda_max = re.findall("([0-9]*)G", line)[0]
        sda_usage = re.findall("([0-9]*)G", line)[1]
    elif (re.search("sdb1", line)):
        sdb_max = re.findall("([0-9]*)G", line)[0]
        sdb_usage = re.findall("([0-9]*)G", line)[1]
    elif (re.search("sdc1", line)):
        sdc_max = re.findall("([0-9]*)G", line)[0]
        sdc_usage = re.findall("([0-9]*)G", line)[1]


sda_output = f"{sda_usage}/{sda_max} G"
sdb_output = f"{sdb_usage}/{sdb_max} G"
sdc_output = f"{sdc_usage}/{sdc_max} G"


command_output = sp.Popen(['uname', '-srm'], stdout=sp.PIPE, stderr=sp.STDOUT)
output, error = command_output.communicate()
decoded_output = output.decode().split()
kernel = decoded_output[1]

def init_bar():


    return bar.Bar(
                    [
                        widget.Image(filename="~/Pictures/qtile_icons/python_logo.png", margin_x=5),
                        widget.GroupBox(inactive='ffffff', highlight_method="block", this_current_screen_border='A93500', this_screen_border='A93500'),
                        widget.Prompt(),
                        widget.CurrentLayout(),
                        widget.Sep(linewidth=670, background='111212', foreground='111212'),
                        widget.Sep(linewidth=20, background='111212', foreground='111212'),
                        widget.Sep(linewidth=15, background='111212', foreground='111212'),
                        widget.Sep(linewidth=20, background='111212', foreground='111212'),
                        widget.Chord(
                            chords_colors={
                                'launch': ("#ff0000", "#ffffff"),
                            },
                            name_transform=lambda name: name.upper(),
                        ),
                        # widget.TextBox("default config", name="default"),
                        # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Image(filename="~/Pictures/qtile_icons/linux_logo.png", margin_x=5),
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.TextBox(fmt=kernel, foreground="ffffff"),
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.Image(filename="~/Pictures/qtile_icons/cal_icon.png", margin_x=5),
                        widget.Clock(format=' %Y-%m-%d %a %I:%M %p '),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),                    
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.Image(filename="~/Pictures/qtile_icons/ssd_icon.png", margin_x=5),
                        widget.TextBox(fmt=sda_output, foreground='62E9E1'),
                        widget.Image(filename="~/Pictures/qtile_icons/hdd_icon.png", margin_x=5),
                        widget.TextBox(fmt=sdb_output, foreground='4e92d0'),
                        widget.TextBox(fmt=sdc_output, foreground='4e92d0'),
                        widget.Sep(linewidth=10, background='111212', foreground='111212', padding=1),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Sep(linewidth=2, background='111212', foreground='111212', padding=1),
                        widget.Image(filename="~/Pictures/qtile_icons/ram_icon.png", margin_x=5),
                        widget.Memory(fmt='{}', foreground='c55050'),
                        widget.Sep(linewidth=10, background='111212', foreground='111212', padding=1),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Sep(linewidth=2, background='111212', foreground='111212', padding=1),
                        widget.Image(filename="~/Pictures/qtile_icons/cpu_icon.png", margin_x=5),
                        widget.CPU(fmt='{}', foreground='EB9B30'),
                    ],
                    24,
                    opacity = 1.00,
                    background='111212',
                )

def init_bar_systray():
    return bar.Bar(
                    [
                        widget.Image(filename="~/Pictures/qtile_icons/python_logo.png", margin_x=5),
                        widget.GroupBox(inactive='ffffff', highlight_method="block", this_current_screen_border='A93500', this_screen_border='A93500'),
                        widget.Prompt(),
                        widget.CurrentLayout(),
                        widget.Sep(linewidth=650, background='111212', foreground='111212'),
                        widget.Sep(linewidth=20, background='111212', foreground='111212'),
                        widget.Sep(linewidth=15, background='111212', foreground='111212'),
                        widget.Sep(linewidth=20, background='111212', foreground='111212'),
                        widget.Chord(
                            chords_colors={
                                'launch': ("#ff0000", "#ffffff"),
                            },
                            name_transform=lambda name: name.upper(),
                        ),
                        # widget.TextBox("default config", name="default"),
                        # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                        widget.Systray(),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Image(filename="~/Pictures/qtile_icons/linux_logo.png", margin_x=5),
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.TextBox(fmt=kernel, foreground="ffffff"),
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.Image(filename="~/Pictures/qtile_icons/cal_icon.png", margin_x=5),
                        widget.Clock(format=' %Y-%m-%d %a %I:%M %p '),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),                    
                        widget.Sep(linewidth=2, background='111212', foreground='111212'), 
                        widget.Image(filename="~/Pictures/qtile_icons/ssd_icon.png", margin_x=5),
                        widget.TextBox(fmt=sda_output, foreground='62E9E1'),
                        widget.Image(filename="~/Pictures/qtile_icons/hdd_icon.png", margin_x=5),
                        widget.TextBox(fmt=sdb_output, foreground='4e92d0'),
                        widget.TextBox(fmt=sdc_output, foreground='4e92d0'),
                        widget.Sep(linewidth=10, background='111212', foreground='111212', padding=1),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Sep(linewidth=2, background='111212', foreground='111212', padding=1),
                        widget.Image(filename="~/Pictures/qtile_icons/ram_icon.png", margin_x=5),
                        widget.Memory(fmt='{}', foreground='c55050'),
                        widget.Sep(linewidth=10, background='111212', foreground='111212', padding=1),
                        widget.Sep(linewidth=0, background='8A8A8B', foreground='8A8A8B', padding=1),
                        widget.Sep(linewidth=2, background='111212', foreground='111212', padding=1),
                        widget.Image(filename="~/Pictures/qtile_icons/cpu_icon.png", margin_x=5),
                        widget.CPU(fmt='{}', foreground='EB9B30'),
                    ],
                    24,
                    opacity = 1.00,
                    background='111212',
                )


screens = [
    Screen( # THIS IS THE RIGHT MONITOR
        top=init_bar_systray(),
    ), 
    Screen( # THIS IS THE MIDDLE MONITOR
        top=init_bar(),
    ), 
     Screen( # THIS IS THE LEFT MONITOR
            top=init_bar(),
        ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
