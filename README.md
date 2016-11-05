WelnessBot
========
based on
 * [HodorBot2](https://github.com/massigrillo/hodorbot2),

Requirements
------------

* [Python 2.7](https://www.python.org/)

* [Virtualenv](https://virtualenv.pypa.io/en/latest/) and [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) ([virtualenvwrapper-win](https://pypi.python.org/pypi/virtualenvwrapper-win) if you're on Windows)

* [Heroku Toolbelt](https://toolbelt.heroku.com/)

* a [Heroku](https://www.heroku.com/) account

* a [Telegram](https://telegram.org/) account

* a REST client ([Postman](https://www.getpostman.com/), for example)

Usage
-----

* chat with [@BotFather](https://telegram.me/BotFather)
    * follow these [instructions](https://core.telegram.org/bots#create-a-new-bot)
    * save the _name_ and the _token_ of your bot

* clone this repository

* add a file named _.env_ in your local repository, containing following code:

        PORT=5000
        TELEGRAM_TOKEN=<your telegram token here>

* open a terminal from your local repository

    * create a virtual environment for your project

            mkvirtualenv hodorbot
            workon hodorbot

    * install dependencies:

            pip install -r requirements.txt

    * execute locally

            heroku local

Deploy
------

* open a terminal from your local repository

    * create a Heroku app

            heroku create

    * providing your credentials when required. Save the name of your app when done.

    * deploy your application to Heroku by pushing to it:

            git push heroku master

    * add postgresql to your app

            heroku addons:create heroku-postgresql:hobby-dev

    * add a configuration variable to your app

            heroku config:set TELEGRAM_TOKEN=<your telegram token here>

* send a GET request
    * to url

            https://api.telegram.org/bot<your telegram token here>/setWebhook?url=https://<your heroku app name>.herokuapp.com/hodor/<your telegram token here>

* start talking with your bot!

