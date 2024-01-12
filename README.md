# Production Setup
## Build Container
`
docker build -t moochi_api --build-arg OPENAI_API_KEY=****************** .
`

## Run Container Command
`docker run -d -p 8000:5000 --memory="2000m" --restart unless-stopped --name moochi_api -it moochi_api`


# Development Setup

## Install Dependencies
`pip3 install -r requirements.txt`

## Set OpenApi Environment Variable
`export OPENAI_API_KEY=******************`

Or for Windows

`SET OPENAI_API_KEY=******************`

## Start Server
`waitress-serve --port=5000 --call api:start_server`