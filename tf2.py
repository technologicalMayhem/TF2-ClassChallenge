import os
import random
import re
import time
from pygame import mixer

# Change these
username = "username" # Your username in-game
log_location = "/home/user/.local/share/Steam/steamapps/common/Team Fortress 2/tf/game.log" # The path to the log file
playing_to = 5 # The amount of kills needed to reach to advance to the next class

classes = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy"]
KILL_REGEX = re.compile('(.+) killed (.+) with .+\\.')
CHANGE_REGEX = re.compile('I am now playing (.+)\\.')

def main():
    while not os.path.exists(log_location):
        time.sleep(1)  # Wait for 1 second before checking again
    
    challenge_class = 0
    game_class = 0
    current_kills = 0
    class_picked = True

    play_audio(classes[challenge_class], "start")
    write_status(challenge_class, current_kills)
    with open(log_location, 'r') as file:
        file.seek(0, 2) # We open the file and go to it's end so we can see new lines coming in
        while True:
            line = file.readline()
            if not line:
                # No new line, wait for a short time before trying again
                time.sleep(0.1)
                continue

            c = CHANGE_REGEX.match(line)
            if c is not None: # We check if the class has been switched
                tf2_class = c.group(1)
                game_class = classes.index(tf2_class)
                print(f"Active class is now {classes[game_class]}")
                if class_picked is False: # We play the 'start' audio snippet once the class is switched to for the first time
                    play_audio(classes[challenge_class], "start")
                    class_picked = True
                    write_status(challenge_class, current_kills)

            m = KILL_REGEX.match(line)
            if challenge_class == game_class and m is not None: # If we are involved in the kill and have the right class we update counters
                killer = m.group(1)
                killed = m.group(2)
                if killer != username and killed != username:
                    continue
                if killed == username: # We have been killed
                    current_kills = 0
                if killer == username: # We killed someone!
                    current_kills += 1
                
                write_status(challenge_class, current_kills)

                if current_kills >= playing_to: # We reached our goal
                    print(f"You finished {classes[challenge_class]}")
                    play_audio(classes[challenge_class], "win")

                    challenge_class += 1
                    class_picked = False

                    if challenge_class == classes.__len__():
                        print("You won!")
                        exit()

                    current_kills = 0

# We create a file writing the current status of the challenge for OBS
def write_status(challenge_class, current_kills):
    status_file = open("status_file.txt", "w")  # write mode
    status_file.write(f"{classes[challenge_class]}: {current_kills} / {playing_to}")
    status_file.close()

# Play the audio for starting and finishing a class
def play_audio(tf2_class, audio_type):
    mixer.init()
    mixer.music.load(get_random_file(f"audio/{tf2_class}/{audio_type}"))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)

# Get a random file from a directory
def get_random_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None
    
    return os.path.join(directory, random.choice(files))

if __name__ == "__main__":
    main()
