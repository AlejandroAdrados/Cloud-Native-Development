FROM node:16

RUN apt-get update && apt-get install -y jq
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm ci
COPY . .
EXPOSE 3000
ENTRYPOINT [ "./entrypoint.sh" ]
