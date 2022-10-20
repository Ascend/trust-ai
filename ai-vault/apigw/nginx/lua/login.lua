local base64 = require("ngx.base64")
local common = require("common")
local cjson = require("cjson")

local function create_session(resp)
    local session = {}
    session.DomainID = resp.UserID
    session.UserID = resp.UserID
    session.RoleID = resp.RoleID
    session.SessionID = common.random(32)
    session.Token = common.random(32)
    return session
end

-- TODO: 增加ip锁

if ngx.req.get_method() ~= "POST" then
    -- TODO: 增加认证次数限制
    ngx.log(ngx.ERR, "Login method is not allow")
    ngx.exit(ngx.HTTP_NOT_ALLOWED)
end

ngx.req.read_body()
local body = ngx.req.get_body_data()
local res, err = ngx.location.capture("/internal/login", {method=ngx.HTTP_POST, body=body, ctx=ngx.ctx})
if not res then
    ngx.log(ngx.WARN,"failed to request: ", err)
    ngx.exit(401)
end
ngx.status = res.status
if ngx.status ~= 200 then
    ngx.log(ngx.WARN, "ngx.status:"..ngx.status)
      ngx.exit(402)
end
local ok, resp = pcall(cjson.decode, res.body)
if resp.status == "00000000" and ok then
    local sess = create_session(resp.data)
    -- session 15分钟超时
    ngx.shared.session_cache:set(sess.UserID, cjson.encode(sess), 900)

    ngx.req.set_header("UserID", sess.UserID)
    ngx.req.set_header("RoleID", sess.RoleID)
    ngx.req.set_header("DomainID", sess.UserID)
    resp.data["Token"] = sess.Token
    local cookie = "sess=".. sess.SessionID .. "." .. sess.UserID .."; Max-Age=900000"
    ngx.header["Set-Cookie"] = cookie .. "; Path=/; Secure=false; SameSite=Strict; HttpOnly"
    ngx.header["Content-Type"] = "application/json"
    ngx.say(cjson.encode(resp))
    ngx.log(ngx.NOTICE, "Login success")
else
    resp={}
    resp["info"] = "failed"
    ngx.status = ngx.HTTP_UNAUTHORIZED
    if res and res.body then
        resp["msg"] = res.body
    end
    ngx.say(cjson.encode(resp))
    ngx.log(ngx.ERR, "Login failed")
end