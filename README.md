BRC
====

Setting up your dev environment:
----
*On Linux (assumes your package manager is apt and your repos are up to date)*

1. Install Python2.7, git, and virtualenv *sudo apt-get install python2.7 virtualenv git*

2. Create a folder for BRC

3. Create a virtual environment *virtualenv brcenv*

4. Activate the virtual environment *source brcenv/bin/activate*

5. Install Django on your virtual environment *pip install django*

*On Windows*

*On Mac*


Getting the code:
----
1. Fork the code from github *On BRC's github page, click the "Fork" on the top right*

2. Download the code from github *On linux terminal: git clone https://github.com/YOUR_GITHUB_USERNAME/brc.git*

3. *OPTIONAL* Add other contributer's forks *On linux terminal: git remote add ANY_NAME https://github.com/OTHER_GITHUB_USERNAME/brc.git*

Running for development:
----
1. Activate your virtual environment *source brcenv/bin/activate from your BRC directory*

2. Change directory to your BRC code *cd brc*

3. Create the database *python manage.py syncdb*

4. Run the server *python manage.py runserver*
