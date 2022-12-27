package utils

import (
	"fmt"
	expect "github.com/Netflix/go-expect"
	"log"
	"os"
	"unsafe"
)

const (
	mkInfo   = "Please input mk to decrypt psk info, and end with a new line."
	certInfo = "Please input password to decrypt private key info, and end with a new line."
	helpMsg  = `
	Usage ./ai-tool [options]
	
	ai-tool options:
		enc   -p  passwd 	ca private key password should satisfy requirements, -p is optional
		dec   path    		encrypted password file path (optional)
		run   cfs_cmd           run cfs service
		h          	        print help message`
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
	ch <- true
	_, err := console.ExpectString(mkInfo)
	if err != nil {
		fmt.Printf("func console ExpectString mkInfo failed with err: %v\n", err.Error())
	}
	ch <- true

	_, err = console.ExpectString(certInfo)
	if err != nil {
		fmt.Printf("func console ExpectString certInfo failed with err: %v\n", err.Error())
	}
	ch <- true

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

// PrintErrExit print error and exit
func PrintErrExit(e error) {
	if e != nil {
		log.Println("Error ", e)
		os.Exit(-1)
	}
}

// PrintHelp print help info
func PrintHelp() {
	fmt.Println(helpMsg)
}

// ClearStringMemory clear sensitive string
func ClearStringMemory(s string) {
	if len(s) <= 1 {
		return
	}
	bs := *(*[]byte)(unsafe.Pointer(&s))
	for i := 0; i < len(bs); i++ {
		bs[i] = 0
	}
}

// CheckPasswd check passwd
func CheckPasswd(p []byte) error {
	if len(p) == 0 {
		return fmt.Errorf("password can not be empty")
	}
	return nil
}
