import { $get, $post, $delete } from './http';

export function fetchMainKey(params = {}) {
    const url = '/AIVAULT/v1/queryMK'
    return $get(url, params)
}

export function fetchPreSharedKey(params = {}) {
    const url = '/AIVAULT/v1/queryPSK'
    return $get(url, params)
}

export function postMK(params = {}) {
    const url = '/AIVAULT/v1/createMK'
    return $post(url, {
        ...params
    },
    {
        responseType: 'blob'
    });
}

export function postPSK(params = {}) {
    const url = '/AIVAULT/v1/createPSK'
    return $post(url, {
        ...params
    });
}

export function deleteMK(params) {
    const url = '/AIVAULT/v1/deleteMK/' + params
    return $delete(url);
}

export function deletePSK(params) {
    const url = '/AIVAULT/v1/deletePSK/' + params
    return $delete(url);
}