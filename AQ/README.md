# Copy the ip display python file to /bin:
sudo cp -i /path/to/ipconfig.py /bin

# Add A New Cron Job:
sudo crontab -e

# Scroll to the bottom and add the following line (after all the #'s):
# if password is needed, use this version
@reboot echo egh455g4 | sudo -S python3 /bin/ipconfig.py
# else use this instead
@reboot python /bin/ipconfig.py

# Can add “&” at the end of the line means the command is run in the background and it won’t stop the system booting up.

# Reboot for testing
sudo reboot
