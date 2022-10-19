package main

import (
	"embed"
	"encoding/hex"
	"fmt"
	"os"
	"os/exec"
	"time"

	expect "github.com/Netflix/go-expect"
	"golang.org/x/term"

	"ai-tool/common/utils"
	"ai-tool/common/whitebox"
)

const (
	name = "MYKEY"
)

func whiteBoxEncrypt(f *embed.FS) {
	fmt.Println("please input password: ")
	input, err := term.ReadPassword(int(os.Stdin.Fd()))
	defer utils.SensitiveInfoClear(input)
	if err != nil {
		fmt.Printf("get the password failed, err: %v", err.Error())
		return
	}
	cipherText, err := whitebox.EncryptBytes(input, f)
	if err != nil {
		fmt.Printf("func EncryptDataInfo run failed, err: %v", err.Error())
	}
	cipherTextStr := hex.EncodeToString(cipherText)
	fmt.Printf("the cipherText is: %s\n", cipherTextStr)
}

func readCipherText(f *embed.FS) ([]byte, error) {
	cipherTextStr := os.Getenv(name)
	cipherText, err := hex.DecodeString(cipherTextStr)
	if err != nil {
		fmt.Printf("cipherTextStr decode to byte failed, err: %v", err.Error())
		return nil, err
	}
	plainText, err := whitebox.DecryptBytes(cipherText, f)
	if err != nil {
		fmt.Printf("func DecryptDataInfo run failed, err: %v", err.Error())
		return nil, err
	}
	return plainText, nil
}

func whiteBoxDecrypt(cfsPath string, para []string, f *embed.FS) {
	var ch chan bool
	ch = make(chan bool, 1)

	plainText, err := readCipherText(f)
	if err != nil {
		fmt.Printf("func readCipherText failed with err: %v", err.Error())
		return
	}
	defer utils.SensitiveInfoClear(plainText)

	console, err := expect.NewConsole(expect.WithStdout(os.Stdout))
	if err != nil {
		fmt.Printf("get console failed, err: %v", err.Error())
		return
	}
	defer utils.CloseConsole(console)

	cmd := exec.Command(cfsPath, para...)
	cmd.Stdin = console.Tty()
	cmd.Stdout = console.Tty()
	cmd.Stderr = console.Tty()

	go utils.ConsoleShow(console, ch)
	time.Sleep(time.Second)

	err = cmd.Start()
	if err != nil {
		fmt.Printf("cmd Run failed with err: %v\n", err.Error())
		return
	}

	val, ok := <-ch
	if !ok && !val {
		return
	}
	str := string(plainText) + "\n"
	_, err = console.Send(str)
	if err != nil {
		fmt.Printf("cmd Wait failed with err: %v\n", err.Error())
		return
	}

	err = cmd.Wait()
	if err != nil {
		fmt.Printf("cmd Wait failed with err: %v\n", err.Error())
		return
	}
}

//go:embed publicTable
//go:embed privateKey
var f embed.FS

func main() {
	if len(os.Args) < 2 {
		fmt.Println("please input command.")
	}
	act := os.Args[1]
	switch act {
	case "enc":
		whiteBoxEncrypt(&f)
	case "run":
		commands := utils.GetCommand(os.Args)
		whiteBoxDecrypt(os.Args[2], commands, &f)
	default:
		fmt.Println("only support enc or run command.")
	}
}
