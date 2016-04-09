# UB ACM Dynamic website

This website is a strong base for building APIs and implementations for the EBoard and ACM members to easily communicate, learn, and take attendance.

## Setup
For production, look at [Digital Ocean's guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04). Also, look at the `ubacm/settings.py` for the evironment variables needed to successfully set up a production environment.

For development and running locally on your computer, run these steps.

1.  `git clone` the repo, either with SSH or HTTPS.
2.  `cd` into the newly cloned directory
3.  `virtualenv -p python3 venv` This will create a virtual python environment, but make sure virtualenv and python3 are installed; Google it.
4.  `source venv/bin/activate` will start the virtualenv.
5.  `pip install -r requirements.txt` will install the dependencies needed for the project onto the virtualenv.
6.  `python manage.py migrate` will set up the development database
7.  `python manage.py createsuperuser` will create a - guess - A SUPERUSER! for the admin section.
8.  `python manage.py runserver` will start the server.

After setup, you will only need `6` and `8` to make changes to the models and run the server.

NOTE: If you make changes to a model, for it to take effect, run `python manage.py makemigrations` and `python manage.py migrate`  
