FROM ubuntu:latest

ENV TZ=Asia/Karachi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

RUN apt clean && \
	apt update -y && \
	apt dist-upgrade -y && \
	apt upgrade -y && \
    apt install -y python3 python3-pip


COPY . /www

WORKDIR /www

RUN pip3 install -r requirements.txt

ENTRYPOINT ["waitress-serve"]
CMD ["--port=5000", "--call", "api:start_server"]

EXPOSE 5000