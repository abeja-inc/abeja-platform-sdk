// auth-gate.js — Firebase Auth ゲート
// 全ページの <head> に type="module" で読み込む（conf.py の html_js_files 経由）。
// ※ これは「ブラウザ表示のゲート」であり、curl 等は本JSを実行しないので生HTMLは取得可能（緩い認証・想定内）。

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.16.0/firebase-app.js";
import {
  getAuth, onAuthStateChanged, signInWithRedirect, getRedirectResult,
  GoogleAuthProvider, signOut
} from "https://www.gstatic.com/firebasejs/12.16.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDKFZiarqyicE7dQYqHjG363xLVvchro_Y",
  // authDomain は「今開いているドメイン自身」を使う → 1ファイルで全サイト(dev/prod, sdk-spec/developers)対応。
  // 各カスタムドメインを Firebase の Authorized domains に登録しておくこと（redirect の /__/auth/handler が各ドメインで動く）。
  authDomain: window.location.hostname,
  projectId: "apf-mlops-docs",
  appId: "1:529780319156:web:3694bc40744a3c3c8b88e1",
};

const ALLOWED_DOMAIN = "abejainc.com";

// FOUC対策：認証が確定するまで全体を隠す
const root = document.documentElement;
root.style.visibility = "hidden";
// 初期化 throw やコールバック未発火で reveal に到達しないと白画面のまま固まる。
// UXゲートなので fail-open（表示側に倒す）。認証確定/拒否時に clearTimeout する。
const failsafe = setTimeout(() => { root.style.visibility = "visible"; }, 8000);
const reveal = () => { clearTimeout(failsafe); root.style.visibility = "visible"; };
const deny = (msg) => {
  document.body.innerHTML =
    `<div style="font:16px/1.6 -apple-system,sans-serif;padding:48px;text-align:center;color:#333">${msg}</div>`;
  reveal();
};

// signOut は onAuthStateChanged を user=null で再発火させる。denied を見ずに
// 再ログインへ飛ばすと拒否画面が定着せずループする（Firebase 公式が警告）。
let denied = false;

try {
  const auth = getAuth(initializeApp(firebaseConfig));

  // リダイレクト戻りを先に処理してから認証状態を判定
  getRedirectResult(auth).catch(() => {}).finally(() => {
    onAuthStateChanged(auth, (user) => {
      if (denied) return;
      if (!user) {
        signInWithRedirect(auth, new GoogleAuthProvider());
        return;
      }
      const email = (user.email || "").toLowerCase();
      const ok = user.emailVerified && email.split("@").pop() === ALLOWED_DOMAIN;
      if (!ok) {
        denied = true;
        signOut(auth).finally(() =>
          deny("このサイトは <b>@abejainc.com</b> の Google アカウントでのみ閲覧できます。"));
        return;
      }
      reveal(); // 認証OK
    });
  });
} catch (e) {
  reveal();
}
