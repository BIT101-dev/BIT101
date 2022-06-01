'''
Author: flwfdd
Date: 2022-03-08 22:30:51
LastEditTime: 2022-06-01 19:51:09
Description:
_(:з」∠)_
'''

redis_host = '127.0.0.1'
redis_port = 6379
ex_time = 24*24*3600

db_url="mysql+pymysql://bitself:password@127.0.0.1/bitself?charset=utf8mb4"

requests_proxy=""
# requests_proxy=""

max_upload_size=24 * 1024 * 1024
img_path="/var/www/html/bitself_img/"
img_url="http://x.x.x.x/bitself_img/"
cos_secret_id=''
cos_secret_key=''
cos_region='ap-beijing'
cos_bucket='bitself-test-1255944436'
cos_path=''

mail_host='smtp.qq.com'
mail_user='bitself@qq.com'
mail_pass=''