import { $get, $post, $delete } from './http';

export function fetchMainKey(params = {},config={}) {
    const url = '/AIVAULT/v1/queryMK'
    return $get(url, params,config)
}

export function fetchPreSharedKey(params = {},config={}) {
    const url = '/AIVAULT/v1/queryPSK'
    return $get(url, params,config)
}

export function postMK(params = {},config={}) {
    const url = '/AIVAULT/v1/createMK'
    return $post(url, {
        ...params
    },
    {
        responseType: 'blob',
        signal : false
    });
}

export function postCert(params = {},config={}) {
  const url = '/certmanager/v1/getcert'
  return $post(url, {
      ...params
    },
    {
      responseType: 'blob',
      signal : false
    });
}

export function postPSK(params = {},config={}) {
    const url = '/AIVAULT/v1/createPSK'
    return $post(url, {
        ...params
    },config);
}

export function deleteMK(params,config={}) {
    const url = '/AIVAULT/v1/deleteMK/' + params
    return $delete(url);
}

export function deletePSK(params,config={}) {
    const url = '/AIVAULT/v1/deletePSK/' + params
    return $delete(url);
}
