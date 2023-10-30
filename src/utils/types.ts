/*
 * @Author: flwfdd
 * @Date: 2023-10-17 13:28:48
 * @LastEditTime: 2023-10-30 18:39:34
 * @Description: _(:з」∠)_
 */


// 帖子
export interface Poster {
    anonymous: boolean; // 是否匿名
    claim: {
        id: number; // 声明id
        text: string; // 声明内容
    }
    comment_num: number; // 评论数量
    create_time: string; // 发布时间
    edit_time: string; // 编辑时间
    id: number;
    images: Image[]; // 图片列表
    like: boolean; // 是否赞过
    like_num: number; // 点赞数量
    own: boolean; // 是否可编辑
    plugins: string; // 插件列表
    public: boolean; // 是否公开
    tags: string[]; // 标签列表
    text: string; // 文本内容
    title: string; // 标题
    update_time: string; // 更新时间
    user: User; // 发布用户
}

// 声明
export interface Claim {
    id: number;
    text: string;
}


// 用户
export interface User {
    avatar: Image; // 头像链接
    create_time: string; // 注册时间
    id: number;
    level: number; // 等级
    motto: string; // 格言 简介
    nickname: string; // 昵称
    identity: {
        color: string; // 勾勾颜色
        text: string; // 用户类型描述
    }
}


// 图片
export interface Image {
    low_url: string; // 低分辨率图片链接
    mid: string; // 图片唯一编码
    url: string; // 原图链接
}

// 评论
export interface Comment {
    id: number; // 评论id
    obj: string; // 评论对象
    text: string; // 评论内容
    images: Image[]; // 图片列表
    user: User; // 评论用户
    anonymous: boolean; // 是否匿名
    create_time: string; // 发布时间
    update_time: string; // 更新时间
    like: boolean; // 是否赞过
    like_num: number; // 点赞数量
    comment_num: number; // 评论数量
    own: boolean; // 是否可删除
    rate: number; // 评分
    reply_user: User; // 回复用户
    reply_obj: string; // 回复对象
    sub: Comment[]; // 子评论
}

