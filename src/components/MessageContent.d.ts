/*
 * @Author: flwfdd
 * @Date: 2022-05-29 17:44:11
 * @LastEditTime: 2022-05-29 17:44:31
 * @Description: 
 * _(:з」∠)_
 */
// 引入naive对应的定义类型
import type { DialogApiInjection } from "naive-ui/lib/dialog/src/DialogProvider";
import type { MessageApiInjection } from "naive-ui/lib/message/src/MessageProvider";

declare global {
    interface Window {
        $message: MessageApiInjection;
        $dialog: DialogApiInjection;
    }
}
