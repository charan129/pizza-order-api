# pizza-order-api

This Project uses docker compose for building the images and starting the services. The requirements for different Operating systems are

Linux - Both docker and docker compose must be installed

windows and macos - only docker desktop needs to be installed

visit the official docker site for instructions on installation https://www.docker.com/

Execute the following command in the project location where yml file is located.   

docker compose up -d

This command will build images and create containers based on the images built. After creating containers, the services will start on the specified ports.

The rabbitmq service will start alongside other services but it will take few minutes to start accepting conncetions.
