export function saveAuthToken(token) {
    sessionStorage.setItem('token', token)
}

export function saveAuthUserInfo(userInfo) {
    sessionStorage.setItem('userInfo', JSON.stringify(userInfo))
}

export function getUserInfo() {
    return JSON.parse(sessionStorage.getItem('userInfo'));
}

export function getAuthToken() {
    return sessionStorage.getItem('token') || '';
}