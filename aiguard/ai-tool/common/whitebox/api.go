package whitebox

import (
	"embed"
	"fmt"

	"ai-tool/common/utils"
)

const blockSize = 16

func EncryptBytes(src []byte, f *embed.FS) ([]byte, error) {
	paddingLen := blockSize - len(src)%blockSize
	if paddingLen == 0 {
		paddingLen = blockSize
	}

	temp := make([]byte, len(src)+paddingLen)
	defer utils.SensitiveInfoClear(temp)
	copy(temp[:len(src)], src)
	temp[len(temp)-1] = byte(paddingLen)

	src_block, dst_block := make([]byte, blockSize), make([]byte, blockSize)
	defer utils.SensitiveInfoClear(src_block)
	defer utils.SensitiveInfoClear(dst_block)

	for cycleTime := 0; cycleTime < len(temp)/blockSize; cycleTime++ {
		start := cycleTime * blockSize
		end := start + blockSize
		copy(src_block[:], temp[start:end])
		if err := encryptBlock(dst_block, src_block, f); err != nil {
			return []byte(nil), err
		}
		copy(temp[start:end], dst_block[:])
	}

	dst := make([]byte, len(temp))
	copy(dst, temp)
	return dst, nil
}

func DecryptBytes(src []byte, f *embed.FS) ([]byte, error) {
	if len(src)%blockSize != 0 {
		return []byte(nil), fmt.Errorf("the decrypt cipher data length must be N*%v", blockSize)
	}

	temp := make([]byte, len(src))
	defer utils.SensitiveInfoClear(temp)
	copy(temp[:len(src)], src)

	src_block, dst_block := make([]byte, blockSize), make([]byte, blockSize)
	defer utils.SensitiveInfoClear(src_block)
	defer utils.SensitiveInfoClear(dst_block)

	for cycleTime := 0; cycleTime < len(temp)/blockSize; cycleTime++ {
		start := cycleTime * blockSize
		end := start + blockSize
		copy(src_block[:], temp[start:end])
		if err := decryptBlock(dst_block, src_block, f); err != nil {
			return []byte(nil), err
		}
		copy(temp[start:end], dst_block[:])
	}

	paddingLen := int(temp[len(temp)-1])
	dst := make([]byte, len(temp)-paddingLen)
	copy(dst, temp[:len(temp)-paddingLen])
	return dst, nil
}
