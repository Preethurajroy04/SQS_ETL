# AWS SQS Data Pipeline to PostgreSQL

This project is a data pipeline that reads messages from an AWS SQS queue, processes and validates the messages, masks sensitive information, and inserts the transformed data into a PostgreSQL database.

## Project Setup

### Requirements
-   Python 3.8 or higher
-   PostgreSQL
-   Docker
-   Docker Compose
-   AWS CLI
-   AWS CLI Local

### Installation Steps
1. Clone the repository and navigate to root directory:
  ```
  git clone https://github.com/Preethurajroy04/SQS_ETL.git
  cd path/to/SQS_ETL
  ```
2. Install dependencies:
  ```
  pip install -r requirements.txt
  ```

3. Setup local development environment:

- Install awscli-local to run AWS CLI commands against LocalStack using test credentials.
  ```
  pip install awscli-local
  ```
- Configure AWS credentials. We can use dummy values since we willl be using LocalStack.
  ```
  aws configure
  ```

  Enter dummy values such as:
  
  ```
  AWS Access Key ID [None]: test
  AWS Secret Access Key [None]: test
  Default region name [None]: us-east-1
  Default output format [None]: json
  ```
- Using Docker Compose:
  
  Ensure Docker is running: Start Docker Desktop on Windows/Mac or ensure Docker daemon is running on Linux.

  Run Docker Compose from the project root directory:
  ```
  docker-compose -f compose.yaml up
  ```

  This will start both the LocalStack and PostgreSQL services. LocalStack will mock AWS services locally, and PostgreSQL will serve as the database.

- Test LocalStack and PostgreSQL services are running.

  Read a message from the queue using awslocal:
  ```
  awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
  ```

  Connect to the Postgres database, verify the table is created
  ```
  psql -d postgres -U postgres -p 5432 -h localhost -W
  ```
  After entering the password <postgres>, run the SQL command:
  ```
  SELECT * FROM user_logins;
  ```

## Running the Application:
1. Execute the main.py script from the project root driectory 'SQS_ETL' to process SQS messages, mask PII data and insert the data into the PostgreSQL database.
   ```
   python main.py
   ```
2. Verify Records in PostgreSQL:
   
   After running the application, verify that the records have been correctly inserted into the PostgreSQL database.
   - Connect to the PostgreSQL database and run the following SQL query:
     ```
     SELECT * FROM user_logins;
     ```
4. Run Unit Test cases:
   
   From the project root directory, run the following command:
   ```
   python -m unittest discover -s tests
   ```
   Ensure all tests pass, indicating that the functionalities like message processing, database insertion, and AWS SQS interactions are working correctly.
   
6. Clean Up:
   
   After verifying the records and running the tests, we can stop the Docker containers to free up resources. Navigate to project root directory and run the following command on a terminal:
   ```
   docker-compose -f compose.yaml down
   ```

## Design Considerations
1. How will you read messages from the queue?
   
      -  In this project, messages are read from the AWS SQS queue using the boto3 library. The get_messages function retrieves up to 10 messages at a time from the specified queue URL. The function uses the receive_message method, which is configured to use LocalStack for local development and testing. This allows the application to efficiently fetch messages in batches, process them, and then delete them from the queue to prevent reprocessing.
2. What type of data structures should be used?

    -  In this project, messages are stored in a list of dictionaries, where each dictionary represents a single message with key-value pairs corresponding to the message    attributes. This format allows for easy access and transformation of the data. After processing, the      transformed data is stored as a list of tuples, where each tuple corresponds to a row of data that will be inserted into the PostgreSQL database. Using dictionaries and tuples provides a clear, structured, and efficient way to manage and process the message data        throughout the application.
3. How will you mask the PII data so that duplicate values can be identified?

    -  PII data is masked using SHA-256 hashing with the hashlib library. This converts sensitive information into consistent hash values, allowing duplicate values to be identified without exposing the original data.
4. What will be your strategy for connecting and writing to Postgres?

    -  The strategy for connecting and writing to PostgreSQL involves using the psycopg2 library. The connection is established once at the start of the application. Processed data is then batched and inserted into the database using a single executemany operation to   
     ensure efficient and secure data insertion. The connection is properly closed after all operations to maintain database integrity and resource management.
           
5. Where and how will your application run?
     -  Currently, the application runs locally. It uses Docker Compose to manage the required services, such as LocalStack for AWS emulation and PostgreSQL for data storage. The script is executed locally, allowing for easy testing and development without the need for a live cloud environment.

## Additional Questions
1. How would you deploy this application in production?
   
     -  We could containerize the application using Docker and deploy it on AWS ECS to ensure scalability and manageability. For workflow orchestration and error handling, we can leverage AWS Step Functions or Apache Airflow. To secure database credentials, we can use AWS Secrets Manager, and place the PostgreSQL database in a secure VPC to restrict access and enhance security.
3. What other components would you want to add to make this production-ready?
     -  Alert/Notification Module: Develop a module that checks for error logs, retrieves root causes of errors, and sends push notifications or emails using AWS SNS for timely incident response.

     -  CI/CD Pipeline: Create a continuous integration and deployment pipeline to automate the containerization of code changes and their deployment to AWS, ensuring rapid and reliable updates.
  
     -  Vormetric Tokenization Server Module: Integrate a Vormetric Tokenization Server to tokenize sensitive PII data, replacing it with secure tokens while allowing for de-tokenization when needed. This enhances data security and helps in complying with data protection regulations.
  
     -  Linters and Code Quality Checks: Integrate linters into the CI/CD pipeline to enforce coding standards and maintain code quality.
       
     -  Automated Unit Tests: Configure the CI/CD pipeline to execute unit tests automatically whenever code changes are approved, ensuring that new changes do not introduce regressions or break existing functionality.

4. How can this application scale with a growing dataset.

     -  Auto-Scaling on AWS: Utilizing AWS Auto Scaling, the application can automatically increase or decrease the number of ECS instances based on the current load, ensuring that it scales dynamically with the dataset.
  
     -  Database Scaling: PostgreSQL can be scaled vertically by increasing the instance size or horizontally by using read replicas to distribute read queries, ensuring that the database can handle a growing dataset efficiently.
  
     -  Kafka: We can transition to kafka if we anticipate needing more advanced message handling capabilities.

5. How can PII be recovered later on?
   
     -  Although not implement in this application, we can use a Vormetric Tokenization Server for securely handling PII through tokenization, which allows both the masking and recovery of original data.

7. What are the assumptions you made?

     -  Database Schema Compatibility: The PostgreSQL table schema matches the message structure.
  
     -  Consistent Message Structure: All received messages have a consistent schema.
  
     -  LocalStack Configuration: LocalStack is correctly set up to emulate required AWS services.
  
     -  No ETL Scheduling Required: There is no requirement to schedule the ETL pipeline; the script runs on-demand.

## Challenges Faced:

  One of the main challenges I encountered was compatibility issues between LocalStack and AWS CLI. The LocalStack version I was using was not compatible with AWS CLI versions higher than 1.3. To address this, I        had to downgrade AWS CLI to version 1.22, which resolved the compatibility issues and allowed me to proceed with the integration and testing of our application. This process involved ensuring that all dependencies        were correctly aligned and that the system configurations supported the downgraded CLI version.