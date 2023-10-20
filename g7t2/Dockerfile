FROM localstack/localstack:latest


# Install node
RUN apt-get install -y curl && \
  curl -sL https://deb.nodesource.com/setup_11.x  | bash - && \
  apt-get -y install nodejs

# Install cdklocal cli
RUN npm i -g aws-cdk-local aws-cdk

COPY requirements.txt /usr/src/backend/requirements.txt
# Install python dependencies so cdk can build
RUN pip install -r /usr/src/backend/requirements.txt

COPY . /usr/src/backend

# Set entrypoint to custom script
RUN mv /usr/local/bin/docker-entrypoint.sh /usr/local/bin/localstack-entrypoint.sh

# copy `docker-entrypoint.sh` script
ADD docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh
