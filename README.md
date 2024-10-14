# What is this?
This is a python script that automates tracking your kills for a challenge in TF2 where you have to get 5 kills with each class, in order, in under one hour. DougDoug came up with this challenge and I decided to make a script for it to try to learn some python.

This also plays a little audio snippet whenever you finish a challenge and pick the next class.

# How does this work?
This uses a couple of config files for TF2. First up in `autoexec.cfg` it enables logging console output on a file. For each class there is a config file that just echoes a short line to annouce that they have been picked. I use this to detect the current class.

It then read the games log and keeps track of the kills in the current life. Advancing when the goal is reached and playing relevant audio.

# How do I use this?

You need to place the .cfg files either in your TF2's cfg directory. Or if you'd rather not pollute your config files under `tf > custom > tf-challenge > cfg`. Either place works.

Update the script variables at the top. 
- `username` needs to equal your in-game name, so it can be found in the log output.
- `log_location` needs to have the path to the log file. On Linux this would be `/home/user/.local/share/Steam/steamapps/common/Team Fortress 2/tf/game.log`. On Windows it should be `C:/Program Files (x86)/Steam/SteamApps/Common/Team Fortress 2/tf/game.log`.
- `playing_to` is the amount of kills need to be reached

The script also creates a file called `status_file.txt` that can be used to display the current status in OBS.