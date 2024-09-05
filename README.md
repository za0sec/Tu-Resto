TuResto Backend Service
=======================

## Requirements

* Python 3.10.4+
* PostgreSQL: [macOS](http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/), [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

## Installation

#### Initialize your Virtual Environment

    python3.10 -m venv .venv --prompt$(basename $(pwd))

#### Activate the Virtual Environment

    source .venv/bin/activate

#### Initialize app requirements (once the Virtual Environment is active)

    python -m pip install --upgrade pip
    pip install --upgrade setuptools wheel
    pip install -r requirements.txt

### Running the projects on localhost

If you have a user for the server, generate a fresh snapshot of the database and follow the instructions in the command output to load it.

```
fab dumpdb
```

**Important** in order for dumpdb to work correctly, you must have a .pgpass file in your home folder. See [this article](https://blog.sleeplessbeastie.eu/2014/03/23/how-to-non-interactively-provide-password-for-the-postgresql-interactive-terminal/) on how to write one.

Finally, run the application:

```
python manage.py runserver
```

## Deployments

Deployments are done automatically by our CI/CD infrastructure now.
Every commit you push to the `main` branch will be automatically
deployed to production.
