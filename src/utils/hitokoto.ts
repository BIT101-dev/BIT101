/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-05-29 13:11:17
 * @Description: 
 * _(:з」∠)_
 */
import { ref } from 'vue'
import http from '@/utils/request';
const hitokoto = ref("")

function UpHitokoto() {
  http.get("https://v1.hitokoto.cn/")
    .then((res) => {
      hitokoto.value = res.data.hitokoto + "  ——" + res.data.from;
    })
}

UpHitokoto();
setInterval(UpHitokoto, 10 * 1000);

export default hitokoto