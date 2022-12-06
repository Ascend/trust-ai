package utils

import (
	"fmt"
	"log"
	"os"
	"unsafe"
)

const (
	helpMsg = `
	Usage ./ai-tool-cfs [options]
	
	ai-tool-cfs options:
		enc   passwd  ca私钥口令需要满足复杂要求
		dec   path    加密口令存放路径(可选）
		h          	  打印帮助信息
`
)

func PrintErrExit(e error) {
	if e != nil {
		log.Println("Error", e)
		os.Exit(-1)
	}
}

func PrintHelp() {
	fmt.Println(helpMsg)
}

// SensitiveInfoClear clear sensitive info
func SensitiveInfoClear(s []byte) {
	for index := 0; index < len(s); index++ {
		s[index] = 0
	}

}

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
