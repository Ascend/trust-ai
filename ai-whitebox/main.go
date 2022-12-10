package main

import (
	"embed"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"os"

	"ai-whitebox/common/utils"
	"ai-whitebox/common/whitebox"
)

const (
	filePath = "/home/AiVault/.ai-vault/encrypted_password"
	fileMode = 0600
)

func whiteBoxEncrypt(p []byte, f *embed.FS) {
	defer utils.SensitiveInfoClear(p)
	cipherText, err := whitebox.EncryptBytes(p, f)
	if err != nil {
		fmt.Printf("encrypt password failed, err: %v", err.Error())
	}
	cipherTextStr := hex.EncodeToString(cipherText)
	fmt.Printf("the cipherText is: %s\n", cipherTextStr)
	// write to file
	if err := ioutil.WriteFile(filePath, cipherText, fileMode); err != nil {
		fmt.Printf("write encrypted password failed, err: %v", err.Error())
	}
}

func readCipherText(path string, f *embed.FS) ([]byte, error) {
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

func whiteBoxDecrypt(path string, f *embed.FS) {
	plainText, err := readCipherText(path, f)
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
		fmt.Println("invalid command.")
		utils.PrintHelp()
		return
	}
	act := os.Args[1]
	switch act {
	case "enc":
		if len(os.Args) < 3 {
			fmt.Println("invalid command.")
			utils.PrintHelp()
			return
		}
		passwd := os.Args[2]
		p := []byte(passwd)
		if err := utils.CheckPasswd(p); err != nil {
			utils.PrintErrExit(err)
		}
		defer utils.ClearStringMemory(passwd)
		whiteBoxEncrypt(p, &f)
	case "dec":
		if len(os.Args) == 3 {
			path := os.Args[2]
			whiteBoxDecrypt(path, &f)
		}
		whiteBoxDecrypt(filePath, &f)
	case "h":
		utils.PrintHelp()
	default:
		fmt.Println("only support enc or dec command.")
		utils.PrintHelp()
	}
}
