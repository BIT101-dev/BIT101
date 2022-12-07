'''
Author: flwfdd
Date: 2022-03-08 22:30:51
LastEditTime: 2022-11-11 11:17:37
Description:
_(:з」∠)_
'''
main_url="http://bit101.cn/#"

redis_host = '127.0.0.1'
redis_port = 6379
ex_time = 24*24*3600

db_url="mysql+pymysql://but101:password@127.0.0.1/bit101?charset=utf8mb4"

requests_proxy=""

page_size=24

max_upload_size=24 * 1024 * 1024
save_path="/var/www/html/bit101/"
save_url="http://x.x.x.x/bit101/"
cos_secret_id=''
cos_secret_key=''
cos_region='ap-beijing'
cos_bucket='bit101-test-1255944436'
cos_path='/'
onedrive_auth_api="https://login.microsoftonline.com/common/oauth2/v2.0/token"
onedrive_api="https://graph.microsoft.com/v1.0/me/drive"
onedrive_client_id=""
onedrive_client_secret=""
onedrive_refresh_token=""

mail_host='smtp.qq.com'
mail_user='bit101@qq.com'
mail_pass=''