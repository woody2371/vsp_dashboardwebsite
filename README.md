This is a Dashboard (written using flask & jinja2 for the API backend, and Vite for the frontend) designed to interface into the Fishbowl Inventory API backend.

Fishwrapper.py is the backend for pulling data, and should be scheduled separately.

Currently shows:

Outstanding Picks - Current items in stock ready to be committed
Committed Sales - Current sales committed in full
Backorders - Items currently out of stock + current inbound stock for those items