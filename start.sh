### 
# @Description: In User Settings Edit
 # @Author: your name
 # @Date: 2019-08-26 10:44:36
 # @LastEditTime: 2019-08-26 10:45:11
 # @LastEditors: Please set LastEditors
 ###
#/bin/sh
gunicorn -w 4 -b 0.0.0.0:8899 wsgi:app > running.log 2>&1 &