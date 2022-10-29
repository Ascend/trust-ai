# coding: UTF-8
# Copyright (c) 2022. Huawei Technologies Co., Ltd. ALL rights reserved.
import ctypes
import platform
from ctypes import c_char_p, c_void_p, c_uint64, c_int, POINTER


class AES:
    """
    AES GCM wrapper
    """
    EVP_CTRL_AEAD_SET_IVLEN = 0x9
    EVP_CTRL_GCM_GET_TAG = 0x10
    EVP_CTRL_GCM_SET_TAG = 0x11
    AES_128_KEY_LEN = 16
    AES_256_KEY_LEN = 32
    FLAG_ENCRYPT = 1
    FLAG_DECRYPt = 0
    GCM_TAG_LEN = 16
    OPENSSL_SUCCESS = 1
    LIB_NAMES = ['libcrypto.so', 'libcrypto.so.1.1', 'libcrypto.so.10']
    OPENSSL_INIT_FLAG = 0x4e
    libcrypto = None
    ALG = ['aes-128-gcm', 'aes-256-gcm']

    def __init__(self, key: bytes, init_vector: bytes):
        """
        init aes class
        Args:
            key: key for encrypt or decrypt (require bytes)
            init_vector: iv for encrypt or decrypt (require bytes)
        """
        if not isinstance(key, bytes):
            raise ValueError(f"Invalid AES key type {type(key)}, require bytes")
        if not isinstance(init_vector, bytes):
            raise ValueError(f"Invalid AES iv type {type(key)}, require bytes")
        if len(key) == self.AES_128_KEY_LEN:
            self.alg_id = 0
        elif len(key) == self.AES_256_KEY_LEN:
            self.alg_id = 1
        else:
            raise ValueError(f"Invalid AES key length {len(key)}")
        self.key = key
        self.init_vector = init_vector
        self.init_lib()

    @staticmethod
    def init_lib():
        if AES.libcrypto is not None:
            return

        for lib in AES.LIB_NAMES:
            try:
                AES.libcrypto = ctypes.CDLL(lib)
                break
            except OSError:
                continue

        if AES.libcrypto is None:
            raise OSError("can not find libcrypto")

        AES.libcrypto.OPENSSL_config.argtypes = (c_char_p, )

        if hasattr(AES.libcrypto, "OPENSSL_init_"
                                  "crypto"):
            AES.libcrypto.OPENSSL_init_crypto.argtypes = (c_uint64, c_void_p)
            AES.libcrypto.OPENSSL_init_crypto(AES.OPENSSL_INIT_FLAG, None)
        else:
            AES.libcrypto.OPENSSL_add_all_algorithms_conf()
        AES.libcrypto.EVP_CIPHER_CTX_free.argtypes = (c_void_p, )
        AES.libcrypto.EVP_CIPHER_CTX_new.restype = c_void_p
        AES.libcrypto.EVP_CIPHER_CTX_set_padding.argtypes = (c_void_p, c_int)
        AES.libcrypto.EVP_CipherInit_ex.argtypes = (c_void_p, c_void_p, c_void_p, c_char_p, c_char_p, c_int)
        AES.libcrypto.EVP_CipherUpdate.argtypes = (c_void_p, c_char_p, POINTER(c_int), c_char_p, c_int)
        AES.libcrypto.EVP_CipherFinal_ex.argtypes = (c_void_p, c_char_p, POINTER(c_int))
        AES.libcrypto.EVP_get_cipherbyname.restype = c_void_p
        AES.libcrypto.EVP_get_cipherbyname.argtypes = (c_char_p, )
        AES.libcrypto.EVP_CIPHER_CTX_ctrl.argtypes = (c_void_p, c_int, c_int, c_void_p)

    def do_cipher(self, ctx, data, flag, tag=None):
        """
        do cipher operation

        Args:
            ctx: openssl ctx
            data: data need to encrypt or decrypt
            flag: 1 or 0, encrypt or decrypt
            tag: GCM verify tag

        Returns:
            encrypted/decrypted data
        """
        cipher = self.libcrypto.EVP_get_cipherbyname(self.ALG[self.alg_id].encode('utf-8'))
        if cipher is None:
            raise ValueError("decrypt get cipher failed")
        self.libcrypto.EVP_CIPHER_CTX_set_padding(ctx, 0)
        self.libcrypto.EVP_CIPHER_CTX_ctrl(ctx, self.EVP_CTRL_AEAD_SET_IVLEN, len(self.init_vector), None)
        enc_buf = ctypes.create_string_buffer(len(data))
        enc_len = c_int(0)
        self.libcrypto.EVP_CipherInit_ex(ctx, cipher, None, ctypes.c_char_p(self.key),
                                         ctypes.c_char_p(self.init_vector), flag)
        ret = self.libcrypto.EVP_CipherUpdate(ctx, enc_buf, ctypes.byref(enc_len), data, len(data))
        if ret != self.OPENSSL_SUCCESS:
            raise ValueError("cipher update failed")
        output = enc_buf.raw[:int(enc_len.value)]
        if flag == self.FLAG_DECRYPt and tag is not None:
            self.libcrypto.EVP_CIPHER_CTX_ctrl(ctx, self.EVP_CTRL_GCM_SET_TAG, self.GCM_TAG_LEN, ctypes.c_char_p(tag))
        ret = self.libcrypto.EVP_CipherFinal_ex(ctx, enc_buf, ctypes.byref(enc_len))
        if ret == self.OPENSSL_SUCCESS:
            output += enc_buf.raw[:int(enc_len.value)]
            return output
        raise ValueError(f"do cipher failed, flag = {flag}")

    def encrypt(self, data):
        """
        encrypt
        Args:
            data:  data need to encrypt

        Returns:
            encrypted data and GCM tag
        """
        ctx = self.libcrypto.EVP_CIPHER_CTX_new()
        if ctx is None:
            raise ValueError("encrypt init failed")

        tag = ctypes.create_string_buffer(self.GCM_TAG_LEN)
        try:
            output = self.do_cipher(ctx, data, self.FLAG_ENCRYPT)
        except ValueError as value_error:
            self.libcrypto.EVP_CIPHER_CTX_free(ctx)
            raise value_error

        self.libcrypto.EVP_CIPHER_CTX_ctrl(ctx, self.EVP_CTRL_GCM_GET_TAG, self.GCM_TAG_LEN, tag)
        self.libcrypto.EVP_CIPHER_CTX_free(ctx)
        return output, tag.value

    def decrypt(self, data, tag):
        """
        decrypt and verify the tag
        Args:
            data: data need to decrypted
            tag: the GCM verify tag, failed if None

        Returns:
            decrypted data
        """
        ctx = AES.libcrypto.EVP_CIPHER_CTX_new()
        if ctx is None:
            raise ValueError("decrypt init failed")

        try:
            return self.do_cipher(ctx, data, self.FLAG_DECRYPt, tag)
        except ValueError as value_error:
            raise value_error
        finally:
            self.libcrypto.EVP_CIPHER_CTX_free(ctx)




