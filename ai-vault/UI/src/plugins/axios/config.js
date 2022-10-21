export default (axios, config = {}) => {
    const defaultConfig = {
        baseURL: '',
        timeout: 20000,
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        }
    }

    Object.assign(axios.defaults, defaultConfig, config);
    return axios;
}