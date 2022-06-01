/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-06-01 15:45:31
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

function FormatTime(t:number|Date) {
  if(!t)return "No Time";
  if(typeof(t)!='number')t=t.getTime()/1000;
  let dt=new Date().getTime()/1000-t;
  if(dt<60)return Math.round(dt)+"秒前";
  if(dt<60*60)return Math.round(dt/60)+"分钟前";
  if(dt<12*60*60)return Math.round(dt/60/60)+"小时前"

  let now=new Date(t*1000);
  let year = now.getFullYear();
  let month = now.getMonth() + 1;
  let date = now.getDate();
  let hour = now.getHours();
  let minute = now.getMinutes();
  let second = now.getSeconds();
  return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
}

export {
  hitokoto,
  FormatTime
}