import { $get } from './http';

// 查询版本号
export function fetchVersion(params = {}) {
    const url = '/AIVAULT/v1/version/'
    return $get(url, params)
}

// 查询健康状态
export function fetchHealthStatus(params = {}) {
    const url = '/AIVAULT/v1/health'
    return $get(url, params)
}

// 查询证书状态
export function fetchCertStatus(params = {}) {
    const url = '/AIVAULT/v1/certStatus'
    return $get(url, params)
}

// 导出
export function exportFile(params = {}) {
    const url = '/datamanager/v1/export'
    return $get(url, {
        ...params
    },
    {
        responseType: 'blob'
    });
}