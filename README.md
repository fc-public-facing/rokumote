# Rokumote
A test with the kivy framework.  Currently a desktop-based app for controlling a Roku device, with tentative plans for an Android platform version.

## Use
The entrypoint is rokumote_guibuilder.py.

This app is practice with the kivy framework, and is pretty light on functionality.  The goal was to have an app with a GUI that can be controlled with keypresses for convenience.

The look is very rough and designed to make each component easy to see for design assistance.

### Key Commands
#### Naked
```
Up/Down/Left/Right Arrow = up/down/left/right
Enter = select
```
#### Shift+
```
Up/Down = volume up/down
Spacebar = home
```
#### CTRL+
```
m = mute/unmute
Spacebar = play
, (comma) = reverse
. (full stop) = forward
```

## Known Issues
• Pressing the power button when the app is not connected to a Roku device will cause the app to crash.
