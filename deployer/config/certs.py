import glob
import os
import subprocess
import sys


class Cert:
    def __init__(self):
        self.code_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.remoteonly = sys.argv[1]
        self.passin = sys.argv[2]

    def generate_cert(self):
        kmsagent_csr_dir = f"{self.code_dir}/resources/*/opt/tlscert/tmp/kmsagent.csr"
        local_csr_dir = "/opt/tlscert/tmp/kmsagent.csr"
        csr_list = glob.glob(kmsagent_csr_dir)
        if csr_list:
            for i in csr_list:
                subp = self.get_cert(
                    csr_dir=i, out_dir=os.path.dirname(i), passin=self.passin
                )
                if subp.returncode != 0:
                    raise
            if self.remoteonly == "n":
                self.get_cert(
                    csr_dir=local_csr_dir,
                    out_dir=os.path.dirname(local_csr_dir),
                    passin=self.passin,
                )
        else:
            if self.remoteonly == "n":
                subp = self.get_cert(
                    csr_dir=local_csr_dir,
                    out_dir=os.path.dirname(local_csr_dir),
                    passin=self.passin,
                )
                if subp.returncode != 0:
                    raise

    def get_cert(self, csr_dir, out_dir, passin):
        return subprocess.run(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                csr_dir,
                "-CA",
                f"{self.code_dir}/resources/cert/ca.pem",
                "-CAkey",
                f"{self.code_dir}/resources/cert/ca.key",
                "-CAcreateserial",
                "-out",
                f"{out_dir}/kmsagent.pem",
                "-days",
                "3650",
                "-extensions",
                "v3_req",
                "-set_serial",
                "01",
                "-extfile",
                f"{self.code_dir}/config/openssl.cnf",
                "-passin",
                f"pass:{passin}",
            ],
            shell=False,
            capture_output=True,
        )


if __name__ == "__main__":
    cert = Cert()
    cert.generate_cert()
