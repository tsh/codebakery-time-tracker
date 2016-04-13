package main

import (
	"github.com/gorilla/websocket"
	"encoding/json"
	"net/http"
	"fmt"
	"log"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}


var connections = make(map[*websocket.Conn]bool)


func echoHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}

	connections[conn] = true
	fmt.Println(connections)

	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			return
		}

		fmt.Printf("recv: %s\n", message)

		response := map[string]string {"username": "username", "message": string(message)}
		jsonResponse, _ := json.Marshal(response)

		for k, _ := range connections {
			err = k.WriteMessage(messageType, jsonResponse);
			if err != nil {
				fmt.Printf("ERROR at: %s\n", k)
			}
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