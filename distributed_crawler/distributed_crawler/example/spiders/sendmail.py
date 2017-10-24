# -*- coding: utf-8 -*- 
# @Author: Shuang0420 
# @Date: 2016-07-20 18:59:50 
# @Last Modified by:   Shuang0420 
# @Last Modified time: 2016-07-20 18:59:50 

import os
import sys
import time
import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import re


def get_curr_time():
    now = datetime.datetime.now()
    curr_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return curr_time

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendmail(message , plain , to_addr_str, alarm_time):
    from_addr = 'monitor@wezhuiyi.com'
    password = 'Warn!Zhu@Yi#2016$'
    #from_addr = '252618408@qq.com'
    #password = 'zhuxianlian1'
    smtp_server = 'smtp.mxhichina.com'
    smtp_port = 25

    msg = MIMEText(plain , 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr_str
    msg['Subject'] = '%s [%s]' % (message , alarm_time)

    to_addr_vec = to_addr_str.split(';')
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr_vec, msg.as_string())
    server.quit()

def htmlTable(tableRow_list , plain):
    head = '<html><head><title></title></head><body>%s<table border="1" cellpadding=10 cellspacing=0>'%plain.encode('utf-8')
    tail = '</table></body></html>'
    table = ''
    for tableRow in tableRow_list:
        table += '<tr>'
        for unit in tableRow:
            if type(unit) == list:
                table += '<td colspan="%s">%s</td>'%(str(unit[0]) , str(unit[1]))
            else:
                table += '<td>%s</td>'%str(unit)
        table += '</tr>'
    return head+table+tail

def sendHtmlmail(message , plain , row_list, to_addr_str, alarm_time):
    from_addr = 'monitor@wezhuiyi.com'
    password = 'Warn!Zhu@Yi#2016$'
    smtp_server = 'smtp.mxhichina.com'
    smtp_port = 25

    content = htmlTable(row_list , plain)

    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr_str
    msg['Subject'] = '%s [%s]' % (message , alarm_time)

    to_addr_vec = to_addr_str.split(';')
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr_vec, msg.as_string())
    server.quit()


def send_dailyreport():
    from_addr = 'from_email@xxx.com'
    password = 'passord'
    smtp_server = 'smtp.mxhichina.com'
    smtp_port = 25
    to_addr_str = 'to_email@xxx.com;to_email@xxx.com'

    msg = MIMEMultipart('related')
    msg['From'] = from_addr
    msg['To'] = to_addr_str
    subject = '[2016-06-09]xxx运营日报'
    msg['Subject'] = Header(subject, 'utf-8')

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    fd = open('report_monitor.html', 'r')
    mail_msg = fd.read()
    fd.close()

    #png_pattern = re.compile(r"<img class='chart' src='(.*?\.png)' alt=''/>")
    png_pattern = re.compile(r"src='(.*?\.png)'")
    png_file_vec = png_pattern.findall(mail_msg)
    if len(png_file_vec) != 0:
        mail_msg = re.sub(r"(src=')(.*?)(\.png')", r'\1cid:\2\3', mail_msg)

    msg_alternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    for file_name in png_file_vec:
        fd = open(file_name, 'r')
        msg_image = MIMEImage(fd.read())
        fd.close()
        msg_image.add_header('Content-ID', '<%s>' % file_name)
        msg.attach(msg_image)

    to_addr_vec = to_addr_str.split(';')
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr_vec, msg.as_string())
    server.quit()

#if __name__ == '__main__':
    #send_dailyreport()
