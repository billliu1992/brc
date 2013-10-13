BRC
====

Installation:
----
*On Linux*
1. Install Python2.7 and virtualenv *sudo apt-get install python2.7 virtualenv*

2. Create a folder for BRC

3. Create a virtual environment *virtualenv brcenv*

4. Activate the virtual environment *source brcenv/bin/activate*

5. Install Django on your virtual environment *pip install django*

6. Download the code from github *git clone https://github.com/billliu1992/brc.git*

*On Windows*

*On Mac*


Running for development:
----
1. Activate your virtual environment *source brcenv/bin/activate from your BRC directory*

2. Change directory to your BRC code *cd brc*

3. Create the database *python manage.py syncdb*

4. Run the server*python manage.py runserver*
