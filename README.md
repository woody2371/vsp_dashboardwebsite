THIS IS AN UPDATE TO CONVERT DELL TO USE API TO DOWNLOAD DATA INSTEAD OF MANUAL IMPORT

This is a Dashboard (written using flask & jinja2) designed to interface into the Fishbowl Inventory API backend.
You can find the backend files at https://github.com/woody2371/fishbowl-api

Currently shows:

Outstanding Picks - Current items in stock ready to be committed
Committed Sales - Current sales committed in full
Backorders - Items currently out of stock + current inbound stock for those items