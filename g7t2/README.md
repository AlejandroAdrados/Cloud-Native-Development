# Welcome to your CDK Python project!

## How to run :running:

To run only the backend either:

- In the root directory, run:
  `make start-backend`
- In the backend directory, run:
  `docker-compose up -d`

To run the entire project:

- `make start-all`
  or
- `docker-compose up -d`
  in the root directory.

:bangbang: **This can show
the error 'exec \<entrypoint file\>: Access is denied.' in the container logs**

**This is likely due to line endings in docker-entrypoint.sh. Make sure the line ends are set to LF and not CRLF (Windows default).**

---

## How to develop :computer:

In the backend directory, start the virtual env:

```
python -m venv .venv      # if there is no .venv folder
source
```

Install the requirements and dev-requirements:

```
pip install -r requirements.txt -r requirements-dev.txt
```

Run as described above.

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

To manually set up the stack locally:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt -r requirements-dev.txt
```

Install localstack:

```
pip install localstack
```

Start localstack (requires docker):

```
localstack start
```

Install aws-cdk-local and aws-cdk globally:

```
npm install -g aws-cdk-local aws-cdk@2.44.0
```

Bootstrap and deploy the stack:

```
cdklocal bootstrap
cdklocal deploy
```

Enjoy!
