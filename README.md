# ETLOne ##
ETLOne is a one stop ETL solution to manage and monitor your workloads. It is a completely serverless framework which uses AWS lambda, S3, AWS glue and Athena to perform ETL for your dataset. The application also provides endpoints using FAST API to predict the output of your ML model.

## Getting Started ##
1. Start docker
2. Clone the repository
3. Run `docker-compose build`
4. Run `docker-compose up -d`

## Steps to perform the ETL ##
1. You need to have an AWS account
2. Go to IAM >> Roles >> Create new role
3. Give Full permission to the following services: CloudWatch, Athena, DynamoDB, S3
4. Create two S3 buckets - `etlone-data-lake-bronze` and `etlone-data-lake-silver`
5. Upload the data file to S3 bucket in `etlone-data-lake-bronze`
6. Now, publish the docker image to AWS ECR using below commands
    ```
    aws ecr get-login-password | docker login --username AWS --password-stdin <your-aws-ecr-ARN>
    docker tag etlone:v1 <your-aws-ecr-ARN>
    docker push <your-aws-ecr-ARN>
    ```
7. Create a new lambda function from ECR image.
8. Add the `custom role` created in step 2 for this lambda service.
9. Add a trigger to the lambda function. The trigger will be for any uploads to `etlone-data-lake-bronze`, the lambda function is invoked and the ETL is run.
10. The transformed data is loaded into `etlone-data-lake-silver`
11. Access the `CloudWatch` logs for results.

## Steps to run the prediction using FAST API ##
1. Run `docker-compose up -d`
2. Open: http://localhost:8008/docs#/
3. Run the POST endpoint - `predict` by selecting  >> Try it Out >> Execute
4. Results will appear in the `Responses` tab.

References:
https://testdriven.io/blog/fastapi-docker-traefik/
https://towardsdatascience.com/7-reasons-why-you-should-consider-a-data-lake-and-event-driven-etl-7616b74fe484
https://medium.com/accenture-the-dock/serverless-api-with-aws-and-python-tutorial-3dff032628a7
https://machinelearningmastery.com/machine-learning-in-python-step-by-step/
https://www.tensorflow.org/tfx/tutorials/serving/rest_simple