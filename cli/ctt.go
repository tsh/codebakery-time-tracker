package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	var user string
//	var password string
	flag.StringVar(&user, "u", "test", "specify username to use")
	flag.Usage = func() {
        fmt.Printf("Usage of %s:\n", os.Args[0])
        fmt.Printf("    username password \n")
        flag.PrintDefaults()
    }
	flag.Parse()
	fmt.Print(user)
	fmt.Printf("other args: %+v\n", flag.Args())
}
