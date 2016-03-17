package main

import (
	"github.com/gorilla/websocket"
	"net/http"
	"fmt"
	"log"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}


func echoHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}

	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			return
		}

		fmt.Printf("recv: %s\n", message)

		err = conn.WriteMessage(messageType, message);
		if err != nil {
			return
		}
	}
}

func main() {
	http.HandleFunc("/echo", echoHandler)
	fmt.Println("Starting...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		panic("Error: " + err.Error())
	}
}