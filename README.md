Freezer Inventory Manager - Installation Guide
Instructions for installing and running the Freezer Inventory Manager app inside Home Assistant as a local Ingress add-on.
Directory Structure in Home Assistant
/addons/freezer_manager/
├── config.json
├── Dockerfile
├── run.sh
├── server.py
└── app/
    └── index.html
Installation Steps
Access your Home Assistant files using the Studio Code Server or Samba share add-on.
Create a folder named freezer_manager inside the /addons directory on your Home Assistant host.
Inside /addons/freezer_manager/, create a subfolder named app.
Copy the code from the Google Docs into their corresponding files:
config.json
Dockerfile
run.sh
server.py
app/index.html
Navigate to Settings > Add-ons > Add-on Store in Home Assistant.
Click the three dots in the top-right corner and select Check for updates / Repositories.
Scroll down to the Local Add-ons section. You will see Freezer Inventory Manager.
Click Install, turn on Show in sidebar, and click Start.
