package main

import (
	"flag"
	"fmt"
	"os"
	"net/http"
	"bytes"
//	"io/ioutil"
	"encoding/json"
	"io/ioutil"
)


type Message struct {
	TimeSpent 	int		`json:"time_spent"`
	Description string	`json:"description"`
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
		fmt.Fprintf(os.Stderr, "%s\n", "User undefined")
		flag.PrintDefaults()
		os.Exit(1)
	}

	if (password == ""){
		fmt.Fprintf(os.Stderr, "%s\n", "Password undefined")
		flag.PrintDefaults()
		os.Exit(1)
	}

	if (timeSpent == -1){
		fmt.Fprintf(os.Stderr, "%s\n", "Time spent not specified")
		flag.PrintDefaults()
		os.Exit(1)
	}

	data, err := ioutil.ReadFile("url.txt")
	url := string(data[:])

//	url := "http://0.0.0.0:8000/api/v1/records/"


	m := Message{TimeSpent: timeSpent, Description: description}
	jm, _ := json.Marshal(m)

    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jm))
    req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(user, password)

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
		fmt.Fprintf(os.Stderr, "\nERROR:  Can't connect to server at: %s\n\n", url)
        panic(err)
    }
    defer resp.Body.Close()

    if resp.StatusCode == 201 {
		fmt.Println("Ok")
	} else {
		fmt.Printf("Smth went wrong! Server returned %s\n", resp.Status)
	}



}
