###
 # @Author: flwfdd
 # @Date: 2023-02-13 19:22:19
 # @LastEditTime: 2023-02-16 23:35:34
 # @Description: 
 # _(:з」∠)_
### 
# gunicorn --certfile=bit101.flwfdd.xyz_bundle.crt --keyfile=bit101.flwfdd.xyz.key --worker-class=gevent --worker-connections=424 --workers=5 -b 0.0.0.0:5554 app:app
gunicorn --worker-class=gevent --workers=5 -b 0.0.0.0:5554 app:app