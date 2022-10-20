local cjson = require("cjson")
local common = require("common")

if ngx.req.get_method() ~= "POST" then
    ngx.log(ngx.ERR, "logout method is not allow")
    ngx.exit(ngx.HTTP_NOT_ALLOWED)
end

local session = common.get_session()

if session == nil then
    ngx.log(ngx.ERR, "invalid cookie")
    local resp = {}
    ngx.header["Content-Type"] = "application/json"
    resp.status = "00000003"
    resp.msg = "please login"
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.say(cjson.encode(resp))
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

local sess = ngx.shared.session_cache:get(session.UserID)
local resp={}
ngx.status = ngx.HTTP_OK
resp["status"] = "00000000"
resp["msg"] = "logout success"
if sess ~= nil then
    ngx.shared.session_cache:delete(session.UserID)
    local cookie = "sess=; Max-Age=0"
    ngx.header["Set-Cookie"] = cookie .. "; Path=/; Secure=false; SameSite=Strict; HttpOnly"
end
ngx.say(cjson.encode(resp))
