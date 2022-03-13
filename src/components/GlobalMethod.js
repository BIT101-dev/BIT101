/*
 * @Author: flwfdd
 * @Date: 2022-03-11 20:54:42
 * @LastEditTime: 2022-03-11 21:42:20
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

export {
    Login
}