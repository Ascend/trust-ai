import axios from 'axios'
import handleResponse from './response'
import handleError from './error'
import setConfig from './config'
import router from '../../router'
export let intactRequest = setConfig(axios);
export let request = intactRequest.create();

// let pendingMap = Map();

request.interceptors.request.use(
    (config) => {
      request.config = Object.assign({}, config);
      return config;
    },
    error => {
      console.log(error) // for debug
      return Promise.reject(error)
    },
  )

request.interceptors.response.use(
    (response) => {
        const { config } = response;
        // pendingMap.delete(config.url);
        return Promise.resolve(handleResponse(response))
    },
    (err) => {
      console.log('接口信息报错' + err) 
      const { config } = request;
      if (!axios.isCancel(err)) {
        // pendingMap.delete(config.url);
      }

      if (!err) return Promise.reject(err);

      if (err.response) {
        err = handleError(err)
        if(err.response.status === 401) {
          router.push('/login')
        }

      } else {
        if (axios.isCancel(err)) {
            throw new axios.Cancel(
                err.message || `请求'${request.config.url}'被取消`
            )
        } else if (err.stack && err.stack.includes('timeout')) {
            err.message = '请求超时';
        } else {
            err.message = '连接服务器失败'
        }
      }
      return Promise.reject(err)
    },
  )