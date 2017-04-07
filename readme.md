HostManage Readme

作者：沈洪斌
博客：http://www.cnblogs.com/vincenshen/


程序介绍：
	1.通过pymysql实现mysql数据库的增删改查
	2.基于ThreadPoolExecutor实现多线程并发paramiko ssh远程执行shell并返回结果
	3.基于rabbitmq实现rpc远程执行shell并返回结果


使用条件：
	1.python3
	2.paramiko模块
	3.pymysql模块
	4.pikam模块
	
	
使用方法：
    1. 使用默认账户alex 123456登录
	2. 输入主机编号选择需要执行shell command的主机，主机编号之间需要使用空格隔开
	3. 输入需要执行的shell命令
	4. 选择paramiko或者rpc的远程调用方式
	5. 输入q退出程序

版本：
     1.1
	
	
更新日志：
v1.0 2017.04.07