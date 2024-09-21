from fabric import Connection, task
import os
from dotenv import read_dotenv

read_dotenv()

@task
def dumpdb(c):
    remote_host = 'turesto.tech'
    remote_user = os.environ.get('SERVER_USERNAME')
    db_name = os.environ.get('DB_NAME', 'turesto')
    db_user = os.environ.get('DB_USER')
    dump_file = 'dump.sql'
    docker_container_name = os.environ.get('DOCKER_CONTAINER_NAME')
    
    if not all([remote_user, db_user, docker_container_name]):
        print("Error: Could not load all necessary environment variables.")
        return
    
    c = Connection(host=remote_host, user=remote_user)

    print("Generating dump file...\nThis could take a while (especially if you're on ITBA's WiFi)")
    
    try:
        c.run(f'docker exec {docker_container_name} pg_dump -U {db_user} -d {db_name} > {dump_file}', hide=True)
        
        c.get(dump_file, local=dump_file)
        print(f"File {dump_file} downloaded locally.")
        
        c.run(f'rm {dump_file}')
        print(f"File {dump_file} removed from remote server.")
    except Exception as e:
        print(f"Error during execution: {str(e)}")
