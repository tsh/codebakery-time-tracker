package main

import (
	"github.com/gorilla/websocket"
	"log"
	"flag"
	"net/url"
)

func main(){
	var addr = flag.String("addr", "localhost:8080", "http service address")
	u := url.URL{Scheme: "ws", Host: *addr, Path: "/echo"}
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()
}
