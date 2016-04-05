package main

import (
	"github.com/gorilla/websocket"
	"log"
	"flag"
	"net/url"
	"fmt"
)

func main(){
	var addr = flag.String("addr", "localhost:8080", "http service address")
	u := url.URL{Scheme: "ws", Host: *addr, Path: "/echo"}
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}

	done := make(chan bool)

	go func() {
		for {
			_, msg, err := c.ReadMessage()
			if err != nil{
				log.Println("err %s", err)
			}
			fmt.Printf("recv: %s", msg)
		}
		done <- true
	}()


	err = c.WriteMessage(websocket.TextMessage, []byte("Hello"))
	if err != nil {
		fmt.Print("error sending message")
	}
	<-done
}
