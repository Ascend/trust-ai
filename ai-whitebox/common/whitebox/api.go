package whitebox

import (
	"embed"
	"fmt"

	"ai-whitebox/common/utils"
)

const blockSize = 16

// EncryptBytes encrypt bytes data
func EncryptBytes(src []byte, f *embed.FS) ([]byte, error) {
	paddingLen := blockSize - len(src)%blockSize
	if paddingLen == 0 {
		paddingLen = blockSize
	}

	temp := make([]byte, len(src)+paddingLen)
	defer utils.SensitiveInfoClear(temp)
	copy(temp[:len(src)], src)
	temp[len(temp)-1] = byte(paddingLen)

	srcBlock, dstBlock := make([]byte, blockSize), make([]byte, blockSize)
	defer utils.SensitiveInfoClear(srcBlock)
	defer utils.SensitiveInfoClear(dstBlock)

	for cycleTime := 0; cycleTime < len(temp)/blockSize; cycleTime++ {
		start := cycleTime * blockSize
		end := start + blockSize
		copy(srcBlock[:], temp[start:end])
		if err := encryptBlock(dstBlock, srcBlock, f); err != nil {
			return []byte(nil), err
		}
		copy(temp[start:end], dstBlock[:])
	}

	dst := make([]byte, len(temp))
	copy(dst, temp)
	return dst, nil
}

// DecryptBytes decrypt bytes data
func DecryptBytes(src []byte, f *embed.FS) ([]byte, error) {
	if len(src)%blockSize != 0 {
		return []byte(nil), fmt.Errorf("the decrypt cipher data length must be N*%v", blockSize)
	}

	temp := make([]byte, len(src))
	defer utils.SensitiveInfoClear(temp)
	copy(temp[:len(src)], src)

	srcBlock, dstBlock := make([]byte, blockSize), make([]byte, blockSize)
	defer utils.SensitiveInfoClear(srcBlock)
	defer utils.SensitiveInfoClear(dstBlock)

	for cycleTime := 0; cycleTime < len(temp)/blockSize; cycleTime++ {
		start := cycleTime * blockSize
		end := start + blockSize
		copy(srcBlock[:], temp[start:end])
		if err := decryptBlock(dstBlock, srcBlock, f); err != nil {
			return []byte(nil), err
		}
		copy(temp[start:end], dstBlock[:])
	}

	paddingLen := int(temp[len(temp)-1])
	dst := make([]byte, len(temp)-paddingLen)
	copy(dst, temp[:len(temp)-paddingLen])
	return dst, nil
}
