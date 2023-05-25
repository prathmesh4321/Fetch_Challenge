# Fetch_Challenge
Receipt Processor Challenge

The webservice is created using Python and Django. 

# INSTRUCTIONS TO RUN THE SERVICE

1. Clone the repository to your local machine.

2. At the root of the working directory run the following docker commands to have the service up and running:

    ```bash

    docker build --tag python-django .

    docker run --publish 8000:8000 python-django

Additional Information:

1. The endpoints can be found in the following file: "receipts/views.py"

2. Use Postman or any other service to test the endpoints.