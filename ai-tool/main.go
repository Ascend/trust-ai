package main

import (
	"embed"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"

	expect "github.com/Netflix/go-expect"
	"golang.org/x/term"

	"ai-tool/common/utils"
	"ai-tool/common/whitebox"
)

const (
	pskName  = "PSK_KEY"
	certName = "CERT_KEY"
	filePath = "/home/AiVault/.ai-vault/encrypted_password"
)

func whiteBoxEncrypt(f *embed.FS) {
	fmt.Println("please input psk password: ")
	inputPskPwd, err := term.ReadPassword(int(os.Stdin.Fd()))
	defer utils.SensitiveInfoClear(inputPskPwd)
	if err != nil {
		fmt.Printf("get the psk password failed, err: %v", err.Error())
		return
	}
	cipherPskPwdText, err := whitebox.EncryptBytes(inputPskPwd, f)
	if err != nil {
		fmt.Printf("func EncryptPskPwdInfo run failed, err: %v", err.Error())
	}

	fmt.Println("please input cert password: ")
	inputCertPwd, err := term.ReadPassword(int(os.Stdin.Fd()))
	defer utils.SensitiveInfoClear(inputCertPwd)
	if err != nil {
		fmt.Printf("get the cert password failed, err: %v", err.Error())
		return
	}
	cipherCertPwdText, err := whitebox.EncryptBytes(inputCertPwd, f)
	if err != nil {
		fmt.Printf("func EncryptCertPwdInfo run failed, err: %v", err.Error())
	}
	cipherPskPwdStr := hex.EncodeToString(cipherPskPwdText)
	cipherCertPwdStr := hex.EncodeToString(cipherCertPwdText)
	fmt.Println("Please use the following command to set environment variables: ")
	fmt.Printf("%s=%s\n", pskName, cipherPskPwdStr)
	fmt.Printf("%s=%s\n", certName, cipherCertPwdStr)
}

func readCipherText(f *embed.FS) ([]byte, []byte, error) {
	cipherPskPwdStr := os.Getenv(pskName)
	cipherPskPwd, err := hex.DecodeString(cipherPskPwdStr)
	if err != nil {
		fmt.Printf("cipherPskPwdStr decode to byte failed, err: %v", err.Error())
		return nil, nil, err
	}
	plainPskPwdText, err := whitebox.DecryptBytes(cipherPskPwd, f)
	if err != nil {
		fmt.Printf("func DecryptPskPwdInfo run failed, err: %v", err.Error())
		return nil, nil, err
	}

	cipherCertPwdStr := os.Getenv(certName)
	cipherCertPwd, err := hex.DecodeString(cipherCertPwdStr)
	if err != nil {
		fmt.Printf("cipherCertPwdStr decode to byte failed, err: %v", err.Error())
		return nil, nil, err
	}
	plainCertPwdText, err := whitebox.DecryptBytes(cipherCertPwd, f)
	if err != nil {
		fmt.Printf("func DecryptCertPwdInfo run failed, err: %v", err.Error())
		return nil, nil, err
	}

	return plainPskPwdText, plainCertPwdText, nil
}

func whiteBoxDecrypt(cfsPath string, para []string, f *embed.FS) {
	var ch chan bool
	ch = make(chan bool, 1)

	PskPwdText, CertPwdText, err := readCipherText(f)
	if err != nil {
		fmt.Printf("func readCipherText failed with err: %v", err.Error())
		return
	}
	defer utils.SensitiveInfoClear(PskPwdText)
	defer utils.SensitiveInfoClear(CertPwdText)

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

	<-ch
	err = cmd.Start()
	if err != nil {
		fmt.Printf("cmd Run failed with err: %v\n", err.Error())
		return
	}

	<-ch
	str := string(PskPwdText) + "\n"
	_, err = console.Send(str)
	if err != nil {
		fmt.Printf("cmd Wait failed with err: %v\n", err.Error())
		return
	}

	<-ch
	str = string(CertPwdText) + "\n"
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

func whiteBoxEncryptP(p []byte, f *embed.FS) {
	defer utils.SensitiveInfoClear(p)
	cipherText, err := whitebox.EncryptBytes(p, f)
	if err != nil {
		fmt.Printf("encrypt password failed, err: %v", err.Error())
	}
	// echo to the console
	fmt.Printf(string(cipherText))
}

func readCipherTextP(path string, f *embed.FS) ([]byte, error) {
	//read cipher password from file
	cipher, err := ioutil.ReadFile(path)
	if err != nil {
		utils.PrintErrExit(err)
	}
	plainText, err := whitebox.DecryptBytes(cipher, f)
	if err != nil {
		fmt.Printf("decrypt cipher failed, err: %v", err.Error())
		return nil, err
	}
	return plainText, nil
}

func whiteBoxDecryptP(path string, f *embed.FS) {
	plainText, err := readCipherTextP(path, f)
	if err != nil {
		fmt.Printf("read cipher data failed: %v", err.Error())
		return
	}
	defer utils.SensitiveInfoClear(plainText)
	fmt.Printf(string(plainText))
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
		if len(os.Args) == 2 {
			whiteBoxEncrypt(&f)
		}
		if len(os.Args) < 4 {
			fmt.Println("invalid command.")
			utils.PrintHelp()
			return
		}
		if os.Args[2] == "-p" {
			passwd := os.Args[3]
			p := []byte(passwd)
			if err := utils.CheckPasswd(p); err != nil {
				utils.PrintErrExit(err)
			}
			defer utils.ClearStringMemory(passwd)
			whiteBoxEncryptP(p, &f)
		}
	case "run":
		commands := utils.GetCommand(os.Args)
		whiteBoxDecrypt(os.Args[2], commands, &f)
	case "dec":
		if len(os.Args) == 3 {
			path := os.Args[2]
			whiteBoxDecryptP(path, &f)
		}
		whiteBoxDecryptP(filePath, &f)
	case "h":
		utils.PrintHelp()
	default:
		fmt.Println("only support enc dec h or run command.")
		utils.PrintHelp()
	}

}
