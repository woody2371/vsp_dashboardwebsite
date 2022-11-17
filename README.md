**Branch to facilitate moving away from using .csv files and moving towards using SQLite to hold data**

This is a Dashboard (written using flask & jinja2) designed to interface into the Fishbowl Inventory API backend.
You can find the backend files at https://github.com/woody2371/fishbowl-api

Currently shows:

Outstanding Picks - Current items in stock ready to be committed
Committed Sales - Current sales committed in full
Backorders - Items currently out of stock + current inbound stock for those items