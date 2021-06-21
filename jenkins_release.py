#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 以上两行代码在linux环境运行时一定要加上，第一行是找到python解释器进行运行py文件，第二行解决编码问题
import jenkins
from jenkins import Jenkins
import eventlet
import time
import logging
import sys

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


class JenkinsBuild:
    def __init__(self, url, username, password):
        # 定义初始
        self.url = url
        self.username = username
        self.password = password

        try:
            # 创建链接
            self.jenkins_con = Jenkins(url=self.url, username=self.username, password=self.password)
            logging.info('jenkins已建立链接')
        except Exception as e:
            logging.info('链接jenkins失败，失败原因：' + str(e))

    def build_job(self, job_name, timeout=300):
        try:
            # 校验jenkins的job是否存在
            self.jenkins_con.assert_job_exists(job_name)
        except jenkins.JenkinsException as e:
            logging.error('job任务不存在: {}'.format(e))

        # 构建任务号
        build_number = self.jenkins_con.get_job_info(job_name)['nextBuildNumber']

        # 启动构建
        self.jenkins_con.build_job(job_name)

        logging.info(f'启动构建任务，任务号{build_number}')

        with eventlet.Timeout(timeout, False):
            is_building = True
            while is_building:
                try:
                    # 判断名为job_name的job是否还在构建中
                    is_building = self.jenkins_con.get_build_info(job_name, build_number).get('building')
                    time.sleep(2)

                    if not is_building:
                        # 获取job_name的某次构建结果
                        result = self.jenkins_con.get_build_info(job_name, build_number).get('result')
                        logging.info('构建结果：' + result)
                        logging.info(self.jenkins_con.get_build_console_output(job_name, build_number))
                        return

                except jenkins.JenkinsException as e:
                    logging.info('{} is not start,waiting.....'.format(build_number))
                    time.sleep(2)

        logging.info('{} jenkins任务，No: {} 构建超时'.format(job_name, build_number))


if __name__ == '__main__':
    # 获取命令行参数 sys.argv[0] 获取操作文件的绝对目录，从1开始依次获取传入的参数
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    job_name = sys.argv[4]

    JenkinsBuild(url=url, username=username, password=password).build_job(job_name)
