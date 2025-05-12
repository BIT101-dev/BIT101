import CryptoJS from 'crypto-js';

export function encryptPassword(password: string, salt: string): string {
    const key = CryptoJS.enc.Base64.parse(salt);
    const encrypted = CryptoJS.AES.encrypt(password, key, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}