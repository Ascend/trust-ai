import { $get, $post, $delete } from './http';

// 查询用户
export function fetchUser(params = {},config = {}) {
    const url = '/usermanager/v1/query'
    return $get(url, params,config)
}

// 删除用户
export function deleteUser(params,config = {}) {
    const url = '/usermanager/v1/user/' + params
    return $delete(url);
}

// 修改密码

export function changePassword(params = {},config = {}) {
    const url = '/usermanager/v1/password'
    return $post(url, {
        ...params
    }, config);
}


// 重置密码
export function resetPassword(params = {},config = {}) {
    const url = '/usermanager/v1/reset'
    return $post(url, {
        ...params
    },config);
}

// 添加用户
export function addUser(params = {},config = {}) {
    const url = '/usermanager/v1/user'
    return $post(url, {
        ...params
    },config);
}
