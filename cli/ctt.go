package main

import (
	"flag"
	"fmt"
	"os"
	"net/http"
	"bytes"
//	"io/ioutil"
	"encoding/json"
)


type Message struct {
	TimeSpent 	int
	Description string
}


func main() {
	var user string
	var password string
	var description string
	var timeSpent int
	flag.StringVar(&user, "u", "", "specify username to login on server")
	flag.StringVar(&password, "p", "", "password to login on server")
	flag.StringVar(&description, "d", "", "description to send")
	flag.IntVar(&timeSpent, "t", -1, "how much time was spent")
	flag.Usage = func() {
        fmt.Printf("Usage of %s:\n", os.Args[0])
//        fmt.Printf("    <username> <password> <description>\nor\n")
        flag.PrintDefaults()
		fmt.Printf("example:\n")
		fmt.Printf(" -u=test -p=test -d=\"some description\"\n")
    }
	flag.Parse()

	if (user == ""){
		fmt.Printf("User undefined\n")
		flag.PrintDefaults()
	}

	if (password == ""){
		fmt.Printf("Password undefined\n")
	}

	if (timeSpent == -1){
		fmt.Printf("Time spent not specified")
	}

	fmt.Printf("DEBUG: other args: %+v\n", flag.Args())

	url := "http://0.0.0.0:8000/api/v1/records/"


	m := Message{TimeSpent: 2, Description: "description"}
	jm, _ := json.Marshal(m)
	js := string(jm)
	fmt.Println(js)

    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jm))
    req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(user, password)

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

//    fmt.Println("response Status:", resp.Status)
//    fmt.Println("response Headers:", resp.Header)
//    body, _ := ioutil.ReadAll(resp.Body)
//    fmt.Println("response Body:", string(body))



}
