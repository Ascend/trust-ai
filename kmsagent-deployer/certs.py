import getpass
import glob
import os
import subprocess


class Cert:
    def __init__(self):
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))

    def generate_cert(self):
        kmsagent_csr_dir = f"{self.cur_dir}/resources/*/opt/tlscert/tmp/kmsagent.csr"
        local_csr_dir = "/opt/tlscert/tmp/kmsagent.csr"
        csr_list = glob.glob(kmsagent_csr_dir)
        if csr_list:
            first_csr_dir = csr_list[0]
            while True:
                passin = getpass.getpass("Enter pass phrase for CAkey:")
                if not passin:
                    continue
                subp = self.get_cert(
                    csr_dir=first_csr_dir,
                    out_dir=os.path.dirname(first_csr_dir),
                    passin=passin,
                )
                if subp.returncode == 0:
                    break
                else:
                    os.unlink(f"{os.path.dirname(first_csr_dir)}/kmsagent.pem")
            for i in csr_list[1:]:
                self.get_cert(csr_dir=i, out_dir=os.path.dirname(i), passin=passin)
            with open(f"{self.cur_dir}/inventory_file", "r", encoding="utf-8") as f:
                if "local" in f.read():
                    self.get_cert(
                        csr_dir=local_csr_dir,
                        out_dir=os.path.dirname(local_csr_dir),
                        passin=passin,
                    )
        else:
            while True:
                passin = getpass.getpass("Enter pass phrase for CAkey:")
                if not passin:
                    continue
                subp = self.get_cert(
                    csr_dir=local_csr_dir,
                    out_dir=os.path.dirname(local_csr_dir),
                    passin=passin,
                )
                if subp.returncode == 0:
                    break
                else:
                    os.unlink(f"{os.path.dirname(local_csr_dir)}/kmsagent.pem")

    def get_cert(self, csr_dir, out_dir, passin):
        return subprocess.run(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                csr_dir,
                "-CA",
                f"{self.cur_dir}/resources/cert/ca.pem",
                "-CAkey",
                f"{self.cur_dir}/resources/cert/ca.key",
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
                f"{self.cur_dir}/openssl.cnf",
                "-passin",
                f"pass:{passin}",
            ],
            shell=False,
            capture_output=True,
        )


if __name__ == "__main__":
    cert = Cert()
    cert.generate_cert()
