import io
import os
import sys

from fabric import task
import dotenv
import dj_database_url


dotenv.read_dotenv()


user = os.environ.get("SERVER_USER")
if not user:
    sys.stderr.write("error: please set SERVER_USER in your .env file\n")
    sys.exit(1)


host = f"{user}@sabf.org.ar:19019"

# run with -e to see each command printed


@task(hosts=[host])
def deploy(c):
    if not os.environ.get("CI"):
        print("Deployment is done automatically from our CI/CD infrastructure now")
        return

    print("Deploying...")

    c.put("scripts/deploy.sh")
    c.sudo("./deploy.sh")


@task(hosts=[host])
def shell(c):
    print("Opening remote shell...")

    c.put("scripts/remote_shell.sh")
    c.run("./remote_shell.sh", pty=True)


@task(hosts=[host])
def dumpdb(c):
    f = io.BytesIO()
    c.get("/srv/apply/.env", f)

    env = dotenv.parse_dotenv(f.getvalue().decode("utf-8"))
    database = dj_database_url.parse(env["DATABASE_URL"])

    print("Generating database dump, this may take a while...")

    cmd = (
        "pg_dump --no-owner --no-acl --host localhost "
        "--dbname {NAME} --username {USER} -w > dump.sql".format(**database)
    )
    try:
        c.run(cmd, pty=True)
    except Exception:  # pylint: disable=broad-except
        print("\nMake sure you have a .pgpass file in your home folder at SABF server")
        return

    print("Downloading database dump...")

    c.get("dump.sql")

    local_env = dotenv.parse_dotenv(open(".env", encoding="utf-8").read())
    local_database = dj_database_url.parse(local_env["DATABASE_URL"])

    print("To restore the database locally, run:")
    print("  psql {NAME} < dump.sql".format(**local_database))
