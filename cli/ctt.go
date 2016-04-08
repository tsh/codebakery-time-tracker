package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	var user string
	var password string
	var description string
	flag.StringVar(&user, "u", "", "specify username to login on server")
	flag.StringVar(&password, "p", "", "password to login on server")
	flag.StringVar(&description, "d", "", "description to send")
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
	} else {
		fmt.Printf("User %s", user)
	}

	if (password == ""){
		fmt.Printf("Password undefined\n")
	}

	fmt.Printf("DEBUG: other args: %+v\n", flag.Args())



}
