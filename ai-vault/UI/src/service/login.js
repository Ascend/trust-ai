import { $get, $post } from './http';

export function sendLogin(params = {}) {
    const { UserName, Password } = params;
    const url = '/api/v1/login';
    return $post(url, {
        UserName,
        Password
    })
}

export function logout() {
    const url = '/api/v1/logout';
    return $post(url)
}