import glob
import os
import subprocess
import sys


class Cert:
    def __init__(self):
        self.code_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.all = sys.argv[1]
        self.passin = sys.argv[2]
        self.type = sys.argv[3]

    def generate_kmsagent_cert(self):
        kmsagent_csr_dir = (
            f"{self.code_dir}/resources/*/opt/aivault_tlscert/tmp/kmsagent.csr"
        )
        local_csr_dir = "/opt/aivault_tlscert/tmp/kmsagent.csr"
        csr_list = glob.glob(kmsagent_csr_dir)
        if csr_list:
            for i in csr_list:
                subp = self.get_cert(
                    csr_dir=i, out_dir=os.path.dirname(i), passin=self.passin
                )
                if subp.returncode != 0:
                    raise
            if self.all == "y":
                self.get_cert(
                    csr_dir=local_csr_dir,
                    out_dir=os.path.dirname(local_csr_dir),
                    passin=self.passin,
                )
        else:
            local_server = False
            with open(f"{self.code_dir}/inventory_file", "r", encoding="utf-8") as f:
                for i in f.readlines():
                    if "local" in i:
                        break
                if "server" in i:
                    local_server = True
            if self.all == "y" and not local_server:
                subp = self.get_cert(
                    csr_dir=local_csr_dir,
                    out_dir=os.path.dirname(local_csr_dir),
                    passin=self.passin,
                )
                if subp.returncode != 0:
                    raise

    def generate_cfs_cert(self):
        cfs_csr_dir = f"{self.code_dir}/resources/*/opt/cfs_tlscert/tmp/kmsagent.csr"
        local_csr_dir = "/opt/cfs_tlscert/tmp/kmsagent.csr"
        csr_list = glob.glob(cfs_csr_dir)
        if csr_list:
            for i in csr_list:
                subp = self.get_cert(
                    csr_dir=i, out_dir=os.path.dirname(i), passin=self.passin
                )
                if subp.returncode != 0:
                    raise
            if self.all == "y":
                self.get_cert(
                    csr_dir=local_csr_dir,
                    out_dir=os.path.dirname(local_csr_dir),
                    passin=self.passin,
                )
        else:
            local_server = False
            with open(f"{self.code_dir}/inventory_file", "r", encoding="utf-8") as f:
                for i in f.readlines():
                    if "local" in i:
                        break
                if "server" in i:
                    local_server = True
            if self.all == "y" and not local_server:
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
    if cert.type == "kmsagent":
        cert.generate_kmsagent_cert()
    if cert.type == "cfs":
        cert.generate_cfs_cert()
