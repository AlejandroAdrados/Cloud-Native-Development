![DSG](./docs/dsg_logo.png)

# Advanced Internet Computing WS 2022 - Group 7 Topic 2

## Overview

The aim of this project was to implement a minimal e-learning platform using a modern serverless architecture and state of the art cloud services. From a user perspective the following major use cases are provided by our platform:

1.  **Register and Login**: For email verification during the registration we included a smtp server in our setup.

2.  **Fetch a new Exercise**: The application supports the types of exercises which are addition, multiplication and derivatives. An exercise is randomly generated, as soon as a user has only a minimal number of exercises left.

3.  **Solve exercise**: The solution of the user is sent to the backend and evaluated for correctness.

4.  **Get Profile**: A user can check his/her profile, which includes a grade for every type of exercise. This graded is a result of the number of correct and incorrect answers of a user.

## Team

- Guillermo Grande: e12202288@student.tuwien.ac.at

- Alejandro López: e12205514@student.tuwien.ac.at

- Nuris Samardzic: e01611855@student.tuwien.ac.at

- Marco Reiser: e11918513@student.tuwien.ac.at

- Jakob Aichinger: e11814579@student.tuwien.ac.at

## Prerequisites

- [Python3](https://www.python.org/downloads/)

- [Node.js](https://nodejs.org/en/download/)

- [aws-cdk-local](https://github.com/localstack/aws-cdk-local)

- [Docker](https://www.docker.com/)

Also, you need to set a valid **localstack pro key** in your environment variables:

```sh
export LOCALSTACK_API_KEY=YOUR_KEY
```

## How to run

Run the docker-compose with:

- Docker compose:

`docker-compose up -d`

OR


- Make:

`make start-all`

Visit the page at `http://localhost:3000`.

This project uses email verification for new registrations. For convenience, a local smtp mock service is used and is available at `http://localhost:3001`. Verification emails are automatically sent to this service.

Have Fun :smile:

## How we tested

For testing we setup a pipeline, which handles the build of our project (frontend and backend service), automatic unit testing and linting of the code. This pipeline runs on a Oracle free tier Cloud Server with the following specifications:

- Type: Cloud

- Hardware: Arm-based Ampere A1 cores and 24 GB of memory

- OS: Oracle Linux

Originally we tried to use the free tier aws micro-instance, however due to the limitation of memory this was not possible.

Additionally, to the pipeline the project was tested locally on every team members machine, which includes the three major operating systems linux, mac os, and windows.

## Architecture

### Services

Our docker-compose file includes of the following three services:

1.  **Localstack**: Serves as our backend service and allows us to deploy various AWS services including Lambda, DynamoDB and SNS/SQS locally on our machine.

2.  **Fronend**: React frontend implementaion.

3.  **SMTP**: Local SMTP server which is used for email verification during registration.

### Data Model

#### Exercise

In our project an exercises is implemented using the Assignment class defined in `g7t2/lambdas/entity/assignment`.

An assignment consists the following four attributes:

1.  **ID**: UUID4 id

2.  **State**: Enum that can be either CORRECT, INCORRECT, or UNSOLVED

3.  **Type**: Enum that can be either ADD, MULT, or DERIV

4.  **Content**: List of numbers.

Depending on the **Type** of the Assignment, an example **content = [7, 2, 4]** is represented as follows:

- **ADD**: $`7 + 2 + 4`$

- **MULT**: $`7 * 2 * 4`$

- **DERIV**: $`7x^2 + 2x + 4`$

Notice, that for the derivative the numbers are the factors and the length-index-1 gives you the power.

### DynamoDB

We use a single table called 'assignments' which stores the following three objects for every user.

1.  **UserId**: UUID of user

2.  **Solved**: A list of assignments of type CORRECT or INCORRECT.

3.  **Unsolved**: A list of assignments of type UNSOLVED.

The idea was that by using two separate lists it is easily possible to verify the number of assignments left.

## How to develop

Requires:

- Python

- Nodejs

Preferrably also _Docker_.

Clone the repository:

`git clone https://hyde.infosys.tuwien.ac.at/aic22/G7T2.git`

Install the requirements. See:

- [Frontend](https://hyde.infosys.tuwien.ac.at/aic22/G7T2/-/tree/develop/frontend)

- [Backend](https://hyde.infosys.tuwien.ac.at/aic22/G7T2/-/tree/develop/g7t2)

After installing the backend requirements, install pre-commit hooks and run on all files:

```
pre-commit install
pre-commit run --all-files
```

Make changes and see them in action:

- With docker (in root directory):

- `docker-compose up -d`

- or `make start-all`

- Or manually: Check [Frontend](https://hyde.infosys.tuwien.ac.at/aic22/G7T2/-/tree/develop/frontend) and [Backend](https://hyde.infosys.tuwien.ac.at/aic22/G7T2/-/tree/develop/g7t2) directories for guides on how to run, lint and test.

On every commit the pre-commit-hooks will run and do basic tasks like linting and formatting.

Since file watching does not work very well on windows the project does not auto-redeploy on changes. Localstack start times can be quite long, therefore the following workflow is recommended to avoid restarting the entire container:

1. Open docker desktop

2. Find the backend/localstack container

3. On the upper right press on the 'Terminal' button

4. Enter `/bin/bash`

5. Enter `cd /usr/src/backend`

6. Enter `cdklocal deploy`

This deploys any changes to the stack to localstack without restarting the localstack service.
