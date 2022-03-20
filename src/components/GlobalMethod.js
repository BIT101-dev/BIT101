/*
 * @Author: flwfdd
 * @Date: 2022-03-11 20:54:42
 * @LastEditTime: 2022-03-19 11:09:10
 * @Description: 
 * _(:з」∠)_
 */
import axios from 'axios'
import store from '@/store'
import { encryptPassword } from "@/components/EncryptPassword";

// 登录模块
async function Login(username, password) {
    let ok = -1;
    let url = store.state.api_url + "/login/init/";
    let execution, encrypted_password, cookie;
    await axios
        .get(url)
        .then((res) => {
            let salt = res.data.salt;
            execution = res.data.execution;
            encrypted_password = encryptPassword(password, salt);
            cookie = res.data.cookie;
            store.commit("set_fake_cookie", "");
            store.commit("set_webvpn_cookie", cookie);
            store.commit("set_webvpn_login", { username: username, password: password });
        })
        .catch((err) => {
            ok = 0;
            console.log(err);
        });

    if (!ok) return ok;
    url = store.state.api_url + "/login/";
    await axios
        .post(url, {
            username: username,
            password: encrypted_password,
            execution: execution,
            cookie: cookie,
        })
        .then((res) => {
            ok = 1;
            store.commit("set_fake_cookie", res.headers["fake_cookie"]);
        })
        .catch((err) => {
            ok = 0;
            console.log(err);
        });
    return ok;
}

function FormatDate(t) {
    if(!t)return "No Time";
    let dt=new Date().getTime()/1000-t;
    //console.log(this.music.name,new Date().getTime(),this.data.play_time);
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
    Login,
    FormatDate,
}