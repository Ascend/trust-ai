local _M = {}
local base64 = require("ngx.base64")
local cjson = require("cjson")
function _M.get_session()
    local cookie_name = "cookie_sess"
    local sessionTag = ngx.var[cookie_name]
    if sessionTag == nil or string.len(sessionTag) == 0 then
        ngx.log(ngx.ERR, "session not exist")
        return nil
    end
    local m = string.gmatch(sessionTag, "([%w_-]+)")
    local session = m()
    local uid = m()
    if session == nil or uid == nil then
        ngx.log(ngx.ERR, "session not exist")
        return nil
    end

    local ngx_session = ngx.shared.session_cache:get(uid)
    if ngx_session == nil then
        ngx.log(ngx.ERR, "session not exist")
        return nil
    end
    local session_info = cjson.decode(ngx_session)
    if session ~= session_info.SessionID then
        ngx.log(ngx.ERR, "session verify failed")
        return nil
    end
--     local token = ngx.req.get_headers()["CSRF-Token"]
--     if token == nil or token ~= session_info.Token then
--         ngx.log(ngx.ERR, "token verify failed")
--         return nil
--     end

    -- 更新session
    ngx.shared.session_cache:expire(uid, 900)
    local cookie = "sess=".. session_info.SessionID .. "." .. session_info.UserID .."; Max-Age=900"
    ngx.header["Set-Cookie"] = cookie .. "; Path=/; Secure=false; SameSite=Strict; HttpOnly"
    for k, v in pairs(session_info) do
        ngx.req.set_header(k, v)
    end
    return session_info
end

function _M.random(len)
    local rand = assert(io.open("/dev/random", "rb"))
    local buf = rand:read(len)
    io.close(rand)
    return base64.encode_base64url(buf)
end

return _M
