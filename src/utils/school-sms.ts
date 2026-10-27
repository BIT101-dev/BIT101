import { reactive } from "vue";

export const schoolSmsState = reactive({
  show: false,
  code: "",
  error: "",
  maskedPhone: "",
  resolve: null as ((code: string) => void) | null,
  reject: null as ((reason: Error) => void) | null,
});

export function requestSchoolSms(maskedPhone: string, error = ""): Promise<string> {
  if (schoolSmsState.resolve) return Promise.reject(new Error("已有待完成的短信验证"));
  return new Promise((resolve, reject) => {
    schoolSmsState.show = true;
    schoolSmsState.code = "";
    schoolSmsState.error = error;
    schoolSmsState.maskedPhone = maskedPhone || "绑定手机";
    schoolSmsState.resolve = resolve;
    schoolSmsState.reject = reject;
  });
}

export function submitSchoolSms() {
  const code = schoolSmsState.code.trim();
  if (!/^\d{4,8}$/.test(code)) {
    schoolSmsState.error = "请输入 4 至 8 位短信验证码";
    return;
  }
  const resolve = schoolSmsState.resolve;
  schoolSmsState.resolve = null;
  schoolSmsState.reject = null;
  schoolSmsState.show = false;
  schoolSmsState.error = "";
  resolve?.(code);
}

export function cancelSchoolSms() {
  const reject = schoolSmsState.reject;
  schoolSmsState.resolve = null;
  schoolSmsState.reject = null;
  schoolSmsState.show = false;
  schoolSmsState.error = "";
  reject?.(new Error("已取消短信验证"));
}
