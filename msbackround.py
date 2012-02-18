import subprocess
import hackthon

networks={"AirBears.Berkeley"}


def check_for_networks():
    process = subprocess.Popen(["ipconfig"],stdout= subprocess.PIPE)
    stdout,stderr = process.communicate()
    for network in networks:
        if network in stdout:
            hackthon.connect()


