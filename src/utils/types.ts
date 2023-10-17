/*
 * @Author: flwfdd
 * @Date: 2023-10-17 13:28:48
 * @LastEditTime: 2023-10-17 13:33:05
 * @Description: _(:з」∠)_
 */

// 帖子
export interface Poster {
    anonymous: boolean; // 是否匿名
    claim: string; // 声明
    comment_num: number; // 评论数量
    create_time: string; // 发布时间
    id: number;
    images: string[]; // 图片链接列表
    like: boolean; // 是否赞过
    like_num: number; // 点赞数量
    public: boolean; // 是否公开
    tags: string[]; // 标签列表
    text: string; // 文本内容
    title: string; // 标题
    update_time: string; // 更新时间
    user: User; // 发布用户
    [property: string]: any;
}

// 用户
export interface User {
    avatar: string;
    create_time: string;
    id: number;
    level: number;
    motto: string;
    nickname: string;
    sid?: string;
    update_time?: string;
    [property: string]: any;
}
