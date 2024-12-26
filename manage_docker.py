import docker

def manage_docker():
    client = docker.from_env()
    
    # Stop all running containers
    for container in client.containers.list():
        print(f'Stopping container: {container.name}')
        container.stop()
    
    # Start containers using docker-compose
    print('Starting containers using docker-compose...')
    import os
    os.system('docker-compose up -d')

if __name__ == "__main__":
    manage_docker()
