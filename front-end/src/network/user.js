import {request} from "@/network/requestConfig.js";

export function loginRequest(data) {
    return request({
        url: '/user/login/',
        method: 'post',
        data
    })
}

// 获取图片验证码
export function getCaptchaRequest() {
    return request({
        url: '/user/captcha/',
        method: 'get'
    })
}

// 发送邮箱验证码
export function sendEmailCodeRequest(data) {
    return request({
        url: '/user/email_code/',
        method: 'post',
        data
    })
}

// 用户注册
export function registerRequest(data) {
    return request({
        url: '/user/register/',
        method: 'post',
        data
    })
}

// 忘记密码邮箱验证码
export function forgetEmailCodeRequest(data) {
    return request({
        url: '/user/forget_email_code/',
        method: 'post',
        data
    })
}

// 忘记密码重置密码
export function resetRequest(data) {
    return request({
        url: '/user/reset/',
        method: 'post',
        data
    })
}

// 个人页 获取用户基本信息
export function getProfileRequest() {
    return request({
        url: '/user/profile/',
        method: 'get'
    })
}

// 个人页 更新用户基本信息
export function updateProfileRequest(data) {
    return request({
        url: '/user/profile/',
        method: 'post',
        data
    })
}

// 个人页 修改密码
export function changePasswordRequest(data) {
    return request({
        url: '/user/change_password/',
        method: 'post',
        data
    })
}