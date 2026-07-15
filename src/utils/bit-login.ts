import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { reactive } from "vue";
import store from "@/utils/store";

type BitLoginService = "jwb" | "jwb_cjd" | "jxzxehall";

interface ChallengeSnapshot {
  challenge_id: string;
  access_token?: string;
  status: "running" | "waiting_sms" | "processing" | "authenticated" | "failed" | "expired";
  requested_services: BitLoginService[];
  ready_services: BitLoginService[];
  expires_in: number;
  masked_phone?: string;
  sms_purpose?: string;
  error?: string;
}

interface ChallengeEnvelope {
  detail?: ChallengeSnapshot;
}

interface Credentials {
  username: string;
  password: string;
}

interface ChallengeSession {
  challengeId: string;
  accessToken: string;
  username: string;
  services: Set<BitLoginService>;
  expiresAt: number;
}

export interface BitLoginAuthResult {
  challengeId: string;
  accessToken: string;
  expiresAt: number;
}

interface SmsPrompt {
  show: boolean;
  code: string;
  error: string;
  maskedPhone: string;
  resolve: ((code: string) => void) | null;
  reject: ((reason: Error) => void) | null;
}

const client = axios.create();
let session: ChallengeSession | null = null;

export const bitLoginState = reactive({
  loading: false,
  sms: {
    show: false,
    code: "",
    error: "",
    maskedPhone: "",
    resolve: null,
    reject: null,
  } as SmsPrompt,
});

function loginUrl(path: string): string {
  return `${store.bit_login_url}${path}`;
}

function challengeHeaders(accessToken: string): Record<string, string> {
  return { "X-Challenge-Token": accessToken };
}

function errorMessage(error: any): string {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (typeof detail?.message === "string") return detail.message;
  return error?.message || "统一身份认证失败";
}

function challengeSnapshot(response: AxiosResponse<ChallengeSnapshot | ChallengeEnvelope>): ChallengeSnapshot {
  const value = response.data;
  if (value && typeof value === "object" && "detail" in value && value.detail) {
    return value.detail;
  }
  return value as ChallengeSnapshot;
}

function isSessionUsable(username: string, services: BitLoginService[]): boolean {
  return Boolean(
    session &&
      session.username === username &&
      session.expiresAt > Date.now() + 5000 &&
      services.every((service) => session?.services.has(service))
  );
}

function updateSession(snapshot: ChallengeSnapshot, username: string): void {
  if (!snapshot.access_token) throw new Error("登录服务未返回 access token");
  session = {
    challengeId: snapshot.challenge_id,
    accessToken: snapshot.access_token,
    username,
    services: new Set(snapshot.ready_services),
    expiresAt: Date.now() + snapshot.expires_in * 1000,
  };
}

function waitForSmsCode(maskedPhone: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const sms = bitLoginState.sms;
    sms.show = true;
    sms.code = "";
    sms.error = "";
    sms.maskedPhone = maskedPhone || "绑定手机";
    sms.resolve = resolve;
    sms.reject = reject;
  });
}

export function submitBitLoginSms(): void {
  const sms = bitLoginState.sms;
  const code = sms.code.trim();
  if (!/^\d{4,8}$/.test(code)) {
    sms.error = "请输入 4 至 8 位短信验证码";
    return;
  }
  const resolve = sms.resolve;
  sms.resolve = null;
  sms.reject = null;
  sms.show = false;
  sms.error = "";
  resolve?.(code);
}

export function cancelBitLoginSms(): void {
  const sms = bitLoginState.sms;
  const reject = sms.reject;
  sms.resolve = null;
  sms.reject = null;
  sms.show = false;
  reject?.(new Error("已取消短信验证"));
}

async function pollChallenge(snapshot: ChallengeSnapshot): Promise<ChallengeSnapshot> {
  if (!snapshot.access_token) throw new Error("登录服务未返回 access token");
  const deadline = Date.now() + Math.max(snapshot.expires_in, 1) * 1000;
  let current = snapshot;
  while (Date.now() < deadline) {
    if (["waiting_sms", "authenticated", "failed", "expired"].includes(current.status)) {
      return current;
    }
    await new Promise((resolve) => window.setTimeout(resolve, 350));
    const response = await client.get<ChallengeSnapshot>(
      loginUrl(`/api/auth/${current.challenge_id}`),
      { headers: challengeHeaders(snapshot.access_token) }
    );
    current = { ...response.data, access_token: snapshot.access_token };
  }
  throw new Error("统一身份认证等待超时，请重试");
}

export async function authenticateBitLogin(
  credentials: Credentials,
  services: BitLoginService[]
): Promise<BitLoginAuthResult> {
  bitLoginState.loading = true;
  try {
    if (isSessionUsable(credentials.username, services)) {
      const current = session as ChallengeSession;
      return {
        challengeId: current.challengeId,
        accessToken: current.accessToken,
        expiresAt: current.expiresAt,
      };
    }

    if (!credentials.password) throw new Error("请重新输入统一身份认证密码");
    session = null;
    let response = await client.post<ChallengeSnapshot | ChallengeEnvelope>(loginUrl("/api/auth/start"), {
      username: credentials.username,
      password: credentials.password,
      services,
      wait_seconds: 1,
    });
    let snapshot = await pollChallenge(challengeSnapshot(response));

    if (snapshot.status === "waiting_sms") {
      const code = await waitForSmsCode(snapshot.masked_phone || "绑定手机");
      response = await client.post<ChallengeSnapshot | ChallengeEnvelope>(
        loginUrl(`/api/auth/${snapshot.challenge_id}/sms`),
        { code },
        { headers: challengeHeaders(snapshot.access_token || "") }
      );
      snapshot = await pollChallenge({
        ...challengeSnapshot(response),
        access_token: snapshot.access_token,
      });
    }

    if (snapshot.status !== "authenticated") {
      throw new Error(snapshot.error || `统一身份认证未完成（${snapshot.status}）`);
    }
    updateSession(snapshot, credentials.username);
    const current = session as ChallengeSession;
    return {
      challengeId: current.challengeId,
      accessToken: current.accessToken,
      expiresAt: current.expiresAt,
    };
  } finally {
    bitLoginState.loading = false;
  }
}

export async function bitLoginRequest<T = any>(
  credentials: Credentials,
  services: BitLoginService[],
  path: string,
  data: Record<string, unknown> = {},
  config: AxiosRequestConfig = {}
): Promise<AxiosResponse<T>> {
  try {
    const auth = await authenticateBitLogin(credentials, services);
    return await client.post<T>(
      loginUrl(path),
      { challenge_id: auth.challengeId, ...data },
      {
        ...config,
        headers: {
          ...config.headers,
          Authorization: `Bearer ${auth.accessToken}`,
        },
      }
    );
  } catch (error) {
    window.$message?.error(errorMessage(error));
    throw error;
  }
}

export function clearBitLoginSession(): void {
  session = null;
}
