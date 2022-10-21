import { $get, $post, $delete } from './http';

// 查询用户
export function fetchUser(params = {}) {
    const url = '/usermanager/v1/query'
    return $get(url, params)
}

// 删除用户
export function deleteUser(params) {
    const url = '/usermanager/v1/user/' + params
    return $delete(url);
}

// 修改密码
export function changePassword(params = {}) {
    const url = '/usermanager/v1/password'
    return $post(url, {
        ...params
    });
}

// 添加用户
export function addUser(params = {}) {
    const url = '/usermanager/v1/user'
    return $post(url, {
        ...params
    });
}
