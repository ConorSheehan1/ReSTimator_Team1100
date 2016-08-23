## How to set up this project locally
1. Run create_db.py
2. Run run.py
3. Open browser and go to localhost:5000

# Important
This project is on a public git repository. If you intend to use it:
* Please use your own secret key and salt (change the values in config.py)
* Please use your own email (change values in config.py)

### Admin users
* Only admin users can create other admin users, so make sure to set up the database with an existing admin user.
1. Go to create_db.py to do this.
2. Change the variable user1 or user2 to your email address and password to make yourself the initial admin.
3. You can then deploy the application and add other admins using the add user feature in the admin section.