FROM golang
RUN mkdir /app
ADD . /app/
WORKDIR /app
RUN go get github.com/gorilla/websocket
CMD ["/data/server.go"]