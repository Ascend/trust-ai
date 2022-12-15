import { $get } from './http';

// 查询版本号
export function fetchVersion(params = {},config={}) {
    const url = '/AIVAULT/v1/version/'
    return $get(url, params,config)
}

// 查询健康状态
export function fetchHealthStatus(params = {},config={}) {
    const url = '/AIVAULT/v1/health'
    return $get(url, params,config)
}

// 查询证书状态
export function fetchCertStatus(params = {},config={}) {
    const url = '/AIVAULT/v1/certStatus'
    return $get(url, params,config)
}

// 导出
export function exportFile(params = {},config={}) {
    const url = '/datamanager/v1/export'
    return $get(url, {
        ...params
    },
    {
        responseType: 'blob',
        signal:false
    });
}

// 数据大小
export function fetchDataSize(params = {},config={}) {
    const url = '/datamanager/v1/size'
    return $get(url, params,config)
}
