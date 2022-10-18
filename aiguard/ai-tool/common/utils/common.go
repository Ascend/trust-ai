package utils

import (
	"fmt"
	"strings"

	expect "github.com/Netflix/go-expect"
)

const (
	info = "Please input mk to decrypt psk info, and end with a new line."
)

// CloseConsole close expect console
func CloseConsole(console *expect.Console) {
	if console != nil {
		err := console.Close()
		if err != nil {
			fmt.Printf("close console failed, err: %v", err.Error())
		}
	}
}

// ConsoleShow show console
func ConsoleShow(console *expect.Console, ch chan bool) {
	data := make([]byte, 1024)
	_, err := console.Read(data)
	if err != nil {
		fmt.Printf("func console Read failed with err: %v\n", err.Error())
		return
	}
	if strings.Contains(string(data), info) {
		ch <- true
	} else {
		fmt.Printf("terminal result is false, data: %s", string(data))
		return
	}

	_, err = console.ExpectEOF()
	if err != nil {
		fmt.Printf("func console ExpectEOF failed with err: %v\n", err.Error())
		return
	}
}

// SensitiveInfoClear clear sensitive info
func SensitiveInfoClear(s []byte) {
	for index := 0; index < len(s); index++ {
		s[index] = 0
	}

}

// GetCommand get cfs command
func GetCommand(arg []string) []string {
	if len(arg) < 3 {
		fmt.Println("please input cfs command follow the run")
	}
	argArray := make([]string, len(arg)-3)
	for i := 3; i < len(arg); i++ {
		argArray[i-3] = arg[i]
	}
	return argArray
}
