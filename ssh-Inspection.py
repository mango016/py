import paramiko
import time
import os
import datetime
import re
os.chdir('D:\python\/log')
today = datetime.date.today().strftime('%Y%m%d')

#这里主要使用锐捷N18012和锐捷RSR7708，所以我是针对这两台设备进行测试
class SSH():
    def __init__(self):
        self.ssh = paramiko
    def login_init(self,ip,username,password):
        self.ip = ip
        print(ip)
        # 实例化一个SSHClient
        self.ssh_client = self.ssh.SSHClient()
        self.ssh_client.set_missing_host_key_policy(self.ssh.client.AutoAddPolicy())
        self.ssh_client.connect(hostname=ip, port=22, username=username, password=password)

    def cmds(self,cmds):
        #self.cmds = cmds
        # 调用invoke_shell()
        # time.sleep更久一些，因为0.1缺数据了……
        command = self.ssh_client.invoke_shell()
        #因为我在交换机没有设置enable 密码，所以我这边是选择直接登录，如果设置了enble密码可自行在cmd文件夹里面添加
        with open(cmds) as rj_cmd :
            for cmd in rj_cmd:
                command.send(cmd.strip() + "\n")
                time.sleep(0.5)
            # 调用makefile，并暂存数据到一个本地变量
            command.close()
            stdout = command.makefile()
            self.echolist = stdout.readlines()

    def filter(self):
        number = 0  # 18012索引标记
        m18012_cpu = []
        cpu_data = []
        memory_data = []
        power_data = []
        fan_data = []
        runing_time = []
        #输出
        with open('log.txt','a') as file_log:
            for e in self.echolist:
                print(e.strip())
                file_log.write(e)
        if 'log.txt' in os.listdir():
            with open('log.txt') as file_log:
                for file in file_log:
                    # N18012**************************************
                    if 'System Memory:' in file:
                        memory = str(re.findall(r"free, (.+?) used", file))  # 使用正则表达式匹配到内存前后关键字
                        print('内存使用率为:', memory[2:7])
                        memory_data.append('内存使用率为:' + memory[2:7])
                    if 'CPU utilization in five minutes:' in file:  # 匹配到指定的设备，要不然会串设备
                        list1 = ['Core_A_防火墙板卡CPU利用率', 'Core_A_M18-8光口板卡CPU利用率', 'Core_A_M18-16口板卡CPU利用率',
                                 'Core_A_M18000-24电-24光口板卡CPU利用率',
                                 'Slot 1/FE1: M18012-FE-D I', 'Slot 1/FE3: M18012-FE-D I', 'Slot 1/M2: M18012-CM II',
                                 'Slot 1/2: RG-WALL 1600-B-ED',
                                 'Slot 2/2: RG-WALL 1600-B-ED', 'Slot 2/4: M18000-08XS-ED', 'Slot 2/7: M18000-16XS2QXS-ED',
                                 'Slot 2/9: M18000-24GT20SFP4XS-ED',
                                 'Slot 2/FE1: M18012-FE-D I', 'Slot 2/FE3: M18012-FE-D I', 'Slot 2/M1: M18012-CM II',
                                 'Slot 2/M2: M18012-CM II', 'Slot 2/2: RG-WALL 1600-B-ED',
                                 'Slot 1/M1_M18012-CM II']
                        m18012_cpu.append(list1[number] + file[31:])  # 板卡型号+cpu使用率
                        if number <= 17:
                            number += 1

                    if '1/1       RG-PA1600I    1600       ok' in file:  # 查看电源
                        print('Core_A_power1:OK')
                        power_data.append('Core_A_power1:OK')

                    if '1/6       RG-PA1600I    1600       ok' in file:
                        print('Core_A_power6:OK')
                        power_data.append('Core_A_power6:OK')

                    if '1/3       RG-PA1600I    1600       ok' in file:
                        print('Core_A_power3:OK')
                        power_data.append('Core_A_power3:OK')

                    if '1/4       RG-PA1600I    1600       ok' in file:
                        print('Core_A_power4:OK')
                        power_data.append('Core_A_power4:OK')

                    if '1/1     ok          normal' in file:
                        print('Core_A_FAN1:OK')
                        fan_data.append('Core_A_FAN1:OK')
                    if '1/2     ok          normal' in file:
                        print('Core_A_FAN2:OK')
                        fan_data.append('Core_A_FAN2:OK')
                    # RSR7708**************************************
                    if '  Used Rate : ' in file:
                        print('内存使用率为:' + file[14:17])
                        memory_data.append('内存使用率为:' + file[14:17])
                    if 'Power-1     RG-PA600-RI       600         OK' in file:
                        print('power1:OK')
                        power_data.append('power1:OK')
                    if 'Power-2     RG-PA600-RI       600         OK' in file:
                        print('power2:OK')
                        power_data.append('power2:OK')
                    # if '1/1    OK' in file:
                    #     fan_data.append('FAN 1/1    OK')
                    # if '1/2    OK' in file:
                    #     fan_data.append('FAN 1/2    OK')
                    # if '1/3    OK' in file:
                    #     fan_data.append('FAN 1/3    OK')
                    # if '1/4    OK' in file:
                    #     fan_data.append('FAN 1/4    OK')
                    # if '1/5    OK' in file:
                    #     fan_data.append('FAN 1/5    OK')
                    # if '1/6    OK' in file:
                    #     fan_data.append('FAN 1/6    OK')
                    # if '1/7    OK' in file:
                    #     fan_data.append('FAN 1/7    OK')
                    # if '1/8    OK' in file:
                    #     fan_data.append('FAN 1/8    OK')
                    # if '1/9    OK' in file:
                    #     fan_data.append('FAN 1/9    OK')
                    # 5750############################################
                    if 'System uptime           :' in file:
                        runing_time.append('设备运行时间:' + file[25:37] + '( day:hours:minutes)')
                    if '1      RG_FAN                          ok ' in file:  # 查看风扇
                        fan_data.append('FAN1:OK')
                    if '2      RG_FAN                          ok ' in file:
                        fan_data.append('FAN2:OK')
                    if '3      RG_FAN                          ok ' in file:
                        fan_data.append('FAN3:OK')
                    # Huawei******************************************
                    # if '(Master) : ' in file:
                    #     print(file[31:66])
                    #     runing_time.append('设备运行时间:' + file[31:66])
                    # if 'tage Is:' in file:
                    #     print(file[29:32])
                    #     memory_data.append('内存使用率：' + file[29:32])
                    # if ': five minutes:' in file:
                    #     print(file[67:70])
                    #     cpu_data.append('CPU使用率:' + file[67:70])

            m18012_cpu = [x.strip() for x in m18012_cpu]  # 去掉列表里的回车
            f = open('巡检' + today + '.txt', 'a+')  # 创建巡检文件，以当前时间命名
            f.write( '管理地址:%s' % self.ip + '设备信息:' + '##' * 25 + '\n'+'\n')  # 设备信息以管理地址+ip分割
            for i in m18012_cpu[0:4]:  # 遍历CPU列表写入文件
                print(i)
                f = open('巡检' + today + '.txt', 'a+')
                f.write(i + '\n' + '\n')
            for i in memory_data:
                f = open('巡检' + today + '.txt', 'a+')
                f.write(i + '\n' + '\n')
            for i in power_data:
                f = open('巡检' + today + '.txt', 'a+')
                f.write(i + '\n' + '\n')
            for i in fan_data:
                f = open('巡检' + today + '.txt', 'a+')
                f.write(i + '\n' + '\n')
            for i in cpu_data:
                f = open('巡检' + today + '.txt', 'a+')
                f.write(i + '\n' + '\n')
            for i in runing_time:
                f = open('巡检' + today + '.txt', 'a+')
                f.write(i + '\n' + '\n')
            f.close()
            os.remove('log.txt')  # 获取数据后删除log文件

if __name__ == '__main__':
    ip_list = 'list.txt'
    username = "xxxx"
    password = "xxxx"
    cmd = 'cmd.txt'
    ssh_login = SSH()
    with open(ip_list,'rt')as ip_obc:
        for ip in ip_obc:
            ssh_login.login_init(ip.strip(),username,password)
            ssh_login.cmds(cmd)
            ssh_login.filter()