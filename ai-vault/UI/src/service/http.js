import { request } from "@/plugins/axios";
import { Message } from "element-ui"; 

function getAuthToken() {
    const token = 'Bearer ' + sessionStorage.getItem('token');
    return token || '';
}

function getError() {
    location.reload();
    sessionStorage.clear();
}

let messageObj = null;
function showErrMsg(message) {
    try {
        messageObj && messageObj.close();
        messageObj = Message.error(message);
    } catch (error) {
        alert(message)
    }
}

export function $get(url, params = {}, config = {}) {
    const { headers, ...rest } = config;
    return new Promise((resolve, reject) => {
      request
        .get(url, {
          params: params,
          headers: {
            Authorization: getAuthToken(),
            ...headers,
          },
          ...rest,
        })
        .then(res => {
          resolve(res)
        })
        .catch(err => {
          reject(err)
            if (err.code == '401' && err.status == '22000001') {
                getError();
            } else {
                showErrMsg(err.message)
            }
        })
    })
}

export function $post(url, params = {}, config = {}) {
    const { headers, ...rest } = config;
    return new Promise((resolve, reject) => {
      request
        .post(url, params, {
            headers: {
                Authorization: getAuthToken(),
                ...headers,
            },
            ...rest,
        })
        .then(res => {
          resolve(res)
        })
        .catch(err => {
          reject(err)
          if (url != '/api/v1/login') {
            if (err.code == '401' && err.status == '22000001') {
                getError();
            } else {
                showErrMsg(err.message)
            }
          }
        })
    })
  }

export function $delete(url, params = {}, config = {}) {
  const { headers, ...rest } = config;
  return new Promise((resolve, reject) => {
    request
      .delete(url, {
          params, 
          headers: {
              Authorization: getAuthToken(),
              ...headers,
          },
          ...rest,
      })
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        reject(err)
          if (err.code == '401' && err.status == '22000001') {
              getError();
          } else {
              showErrMsg(err.message)
          }
      })
  })
}
