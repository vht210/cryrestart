import subprocess
import shlex
from operator import truediv


class RestartDocker(object):
    def __init__(self):
        pass

    def is_err_in_get_lastest_log(self):
        #print("Hello world")
        cmd = "docker logs crynux_node -n 2"
        args = shlex.split(cmd)
        rs = subprocess.Popen(args,stdout = subprocess.PIPE , stderr = subprocess.PIPE)
        ouput,err = rs.communicate()
        print(err)
        if(str(err).find("ERROR")>-1) or (str(err).find("error")> -1) or (str(err).find("Error")> -1) or (str(err).find("kicked")> -1) or (str(err).find("TransactionNotFound")> -1) or (str(err).find("BlockNotFound")> -1) or (str(err).find("node manager is stopped")> -1) :
            return True
        return False

    def get_contain_id(self):
        #cmd = "docker ps -f name=crynux_node"
        cmd= "docker container ls -a -f name=crynux_node"
        args = shlex.split(cmd)
        rs = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = rs.communicate()
        restart=True
        if(str(output).find("Up")==-1):
            restart=False
        if (str(output).find("NAMES")> -1):
            container = str(output).split('NAMES\\n')[-1].split("   ghcr.io")[0]
            print(container)
            return (container,restart)


    def restart_container(self,container_id,is_restart):
        cmd = "docker start " + container_id

        if is_restart:
            cmd= "docker restart " + container_id
        print(cmd)
        args = shlex.split(cmd)
        rs = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = rs.communicate()
        print(output,err)

if __name__ == "__main__":
    rd = RestartDocker()
    container,is_restart=rd.get_contain_id()
    is_err = rd.is_err_in_get_lastest_log()
    if is_err:
        print("Restart " + container + " due to error")
        rd.restart_container(container,is_restart)
#@print("Hello world")
