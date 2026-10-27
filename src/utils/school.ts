import { reactive } from "vue";
import http from "./request";
import { encryptPassword } from "./EncryptPassword";
import { readSchoolCache, removeSchoolCache, schoolSessionKey, writeSchoolCache } from "./school-cache";
import { cancelSchoolSms, requestSchoolSms } from "./school-sms";

interface StoredSchoolSession {
  sid: string;
  cookie: string;
}

const saved = readSchoolCache<StoredSchoolSession>("session")?.data;

export const schoolSession = reactive({
  sid: typeof saved?.sid === "string" ? saved.sid : "",
  cookie: typeof saved?.cookie === "string" ? saved.cookie : "",
  loading: false,
});

interface SchoolVerification {
  token: string;
  code: string;
  webvpn_cookie: string;
}

let pending: { sid: string; request: Promise<SchoolVerification> } | null = null;
let generation = 0;

async function verifySchoolSms(challenge: string, maskedPhone: string): Promise<SchoolVerification> {
  let errorMessage = "";
  while (true) {
    const code = await requestSchoolSms(maskedPhone, errorMessage);
    try {
      const result = await http.post("/user/webvpn_verify_sms", { challenge, code });
      return result.data as SchoolVerification;
    } catch (error: any) {
      errorMessage = error?.response?.data?.msg || "短信验证失败，请重试";
      if (errorMessage !== "短信验证码错误或已失效") throw error;
    }
  }
}

function storeVerification(username: string, data: SchoolVerification, expectedGeneration: number): SchoolVerification {
  if (!data.webvpn_cookie) throw new Error("学校认证未返回有效会话");
  if (!data.token || !data.code) throw new Error("统一身份认证返回的注册信息不完整");
  if (expectedGeneration !== generation) throw new Error("学校会话已变化，请重新认证");
  generation++;
  schoolSession.sid = username;
  schoolSession.cookie = data.webvpn_cookie;
  writeSchoolCache("session", { sid: username, cookie: data.webvpn_cookie });
  return data;
}

export async function verifySchool(sid: string, password: string): Promise<SchoolVerification> {
  const username = sid.trim();
  if (!username) throw new Error("请输入学号");
  if (!password) throw new Error("请输入学校统一身份认证密码");
  if (pending) {
    if (pending.sid === username) return pending.request;
    throw new Error("另一个学校账号正在认证，请稍后重试");
  }
  const expectedGeneration = generation;

  const request = (async () => {
    schoolSession.loading = true;
    try {
      const init = await http.post("/user/webvpn_verify_init", { sid: username });
      const { salt, execution, cookie } = init.data;
      try {
        const result = await http.post("/user/webvpn_verify", {
          sid: username,
          salt,
          execution,
          cookie,
          fingerprint: init.data.fingerprint,
          password: encryptPassword(password, salt),
          captcha: encryptPassword("{}", salt),
        });
        return storeVerification(username, result.data, expectedGeneration);
      } catch (error: any) {
        const challenge = error?.response?.data?.challenge;
        if (error?.response?.status !== 409 || !challenge) throw error;
        const verified = await verifySchoolSms(challenge, error.response.data.masked_phone || "绑定手机");
        return storeVerification(username, verified, expectedGeneration);
      }
    } finally {
      schoolSession.loading = false;
    }
  })();
  pending = { sid: username, request };
  try {
    return await request;
  } finally {
    pending = null;
  }
}

export function hasSchoolCookie(sid: string): boolean {
  return schoolSession.sid === sid.trim() && schoolSession.cookie !== "";
}

export async function getSchoolCookie(sid: string, password: string): Promise<string> {
  const username = sid.trim();
  if (schoolSession.sid && schoolSession.sid !== username) clearSchoolCookie();
  if (hasSchoolCookie(username)) return schoolSession.cookie;
  const result = await verifySchool(username, password);
  return result.webvpn_cookie;
}

export function isSchoolSessionError(error: any): boolean {
  return error?.response?.data?.msg === "未通过身份认证Orz";
}

export function isSchoolAuthRequired(error: any): boolean {
  return isSchoolSessionError(error) ||
    error?.response?.data?.msg === "统一身份认证失败Orz" ||
    error?.message === "学校会话已变化，请重新认证" ||
    error?.message === "请输入学校统一身份认证密码" ||
    error?.message === "请输入学号";
}

function clearSchoolCookieIfMatch(sid: string, cookie: string) {
  if (schoolSession.sid === sid && schoolSession.cookie === cookie) clearSchoolCookie();
}

export async function withSchoolSession<T>(
  sid: string,
  password: string,
  request: (cookie: string) => Promise<T>,
): Promise<T> {
  const username = sid.trim();
  const cookie = await getSchoolCookie(username, password);
  const recoveryGeneration = generation;
  try {
    return await request(cookie);
  } catch (error) {
    if (!isSchoolSessionError(error)) throw error;
    if (schoolSession.sid === username && schoolSession.cookie && schoolSession.cookie !== cookie) {
      const current = schoolSession.cookie;
      try {
        return await request(current);
      } catch (retryError) {
        if (isSchoolSessionError(retryError)) clearSchoolCookieIfMatch(username, current);
        throw retryError;
      }
    }
    if (recoveryGeneration !== generation) throw new Error("学校会话已变化，请重新认证");
    clearSchoolCookieIfMatch(username, cookie);
    const verified = await verifySchool(username, password);
    try {
      return await request(verified.webvpn_cookie);
    } catch (retryError) {
      if (isSchoolSessionError(retryError)) clearSchoolCookieIfMatch(username, verified.webvpn_cookie);
      throw retryError;
    }
  }
}

export function clearSchoolCookie() {
  cancelSchoolSms();
  generation++;
  schoolSession.sid = "";
  schoolSession.cookie = "";
  removeSchoolCache("session");
}

window.addEventListener("storage", (event) => {
  if (event.key !== schoolSessionKey) return;
  cancelSchoolSms();
  generation++;
  const current = readSchoolCache<StoredSchoolSession>("session")?.data;
  schoolSession.sid = current?.sid || "";
  schoolSession.cookie = current?.cookie || "";
});
