import subprocess
import shlex
from operator import truediv


class RestartDocker(object):
    def __init__(self):
        pass

    def is_err_in_get_lastest_log(self):
        #print("Hello world")
        cmd = "docker logs crynux_node -n 1"
        args = shlex.split(cmd)
        rs = subprocess.Popen(args,stdout = subprocess.PIPE , stderr = subprocess.PIPE)
        ouput,err = rs.communicate()
        print(err)
        if(str(err).find("ERROR")>-1) or (str(err).find("error")> -1):
            return True
        return False

    def get_contain_id(self):
        cmd = "docker ps -f name=crynux_node"
        args = shlex.split(cmd)
        rs = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = rs.communicate()
        if (str(output).find("NAMES")> -1):
            container = str(output).split('NAMES\\n')[-1].split("   ghcr.io")[0]
            print(container)
            return container


    def restart_container(self,container_id):
        cmd = "docker restart " + container_id
        args = shlex.split(cmd)
        rs = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = rs.communicate()
        print(output,err)

if __name__ == "__main__":
    rd = RestartDocker()
    container = rd.get_contain_id()
    is_err = rd.is_err_in_get_lastest_log()
    if is_err:
        print("Restart " + container + " due to error")
        rd.restart_container(container)
#@print("Hello world")