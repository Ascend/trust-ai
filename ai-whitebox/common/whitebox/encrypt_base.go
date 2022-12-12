package whitebox

import (
	"crypto/aes"
	"crypto/rand"
	"embed"
	"errors"
	"fmt"
	"io/ioutil"

	"github.com/OpenWhiteBox/AES/constructions/full"
	"github.com/OpenWhiteBox/primitives/encoding"
	"github.com/OpenWhiteBox/primitives/matrix"

	"ai-whitebox/common/utils"
)

// GenerateTable generate whitebox table
func GenerateTable() {
	key := make([]byte, 16)
	rand.Read(key)

	seed := make([]byte, 16)
	rand.Read(seed)

	constr, inputMask, outputMask := full.GenerateKeys(key, seed)

	// Write the public white-box to disk.
	ioutil.WriteFile("./publicTable", constr.Serialize(), 0777)

	// Write the private input and output mask to disk.
	buff := make([]byte, 0)
	buff = append(buff, key...)

	for _, row := range inputMask.Forwards {
		buff = append(buff, row...)
	}
	buff = append(buff, inputMask.BlockAdditive[:]...)

	for _, row := range outputMask.Forwards {
		buff = append(buff, row...)
	}
	buff = append(buff, outputMask.BlockAdditive[:]...)

	ioutil.WriteFile("./privateKey", buff, 0777)
}

func encryptBlock(dst, src []byte, f *embed.FS) error {
	if len(dst) != 16 {
		return errors.New("the length of byte must be 16")
	}
	data, err := f.ReadFile("publicTable")
	if err != nil {
		err = fmt.Errorf("get public Table error: %v", err.Error())
		return err
	}
	c, err := full.Parse(data)
	if err != nil {
		err = fmt.Errorf("parse public Table error: %v", err.Error())
		return err
	}
	temp := [16]byte{}
	defer utils.SensitiveInfoClear(temp[:])

	c.Encrypt(temp[:], src)
	copy(dst, temp[:])

	return nil
}

func decryptBlock(dst, src []byte, f *embed.FS) error {
	if len(dst) != 16 {
		return errors.New("the length of byte must be 16")
	}
	// Read key from disk and parse it.
	data, err := f.ReadFile("privateKey")
	if err != nil {
		err = fmt.Errorf("get private Key error: %v", err.Error())
		return err
	}
	inputLinear, outputLinear := matrix.Matrix{}, matrix.Matrix{}
	inputConst, outputConst := [16]byte{}, [16]byte{}

	key, data := data[:16], data[16:]
	for i := 0; i < 128; i++ {
		inputLinear, data = append(inputLinear, data[:16]), data[16:]
	}
	copy(inputConst[:], data)
	data = data[16:]
	for i := 0; i < 128; i++ {
		outputLinear, data = append(outputLinear, data[:16]), data[16:]
	}
	copy(outputConst[:], data)

	inputMask := encoding.NewBlockAffine(inputLinear, inputConst)
	outputMask := encoding.NewBlockAffine(outputLinear, outputConst)

	// Decrypt block.
	temp := [16]byte{}
	defer utils.SensitiveInfoClear(temp[:])
	copy(temp[:], src)

	temp = outputMask.Decode(temp)
	c, err := aes.NewCipher(key)
	if err != nil {
		return err
	}

	c.Decrypt(temp[:], temp[:])
	temp = inputMask.Decode(temp)
	copy(dst, temp[:])

	return nil
}
