local cjson = require("cjson")
local common = require("common")


local function get_permission(session)
    for k, v in pairs(session) do
        ngx.req.set_header(k, v)
    end
    ngx.log(ngx.ERR, "get_method: "..ngx.req.get_method())
    ngx.log(ngx.ERR, "get_url: "..ngx.var.request_uri)
    local body = {}
    body.FuncName=ngx.req.get_method()
    body.Prefix=ngx.var.request_uri

    local res, err = ngx.location.capture("/internal/getpermission", {
        method=ngx.HTTP_POST,
        ctx=ngx.ctx,
        body=cjson.encode(body)
    })
    ngx.log(ngx.ERR, "body: "..cjson.encode(body))
    if res == nil then
        ngx.log(ngx.ERR, "get permission failed")
        return nil
    end
    local ok, resp = pcall(cjson.decode, res.body)
    if not ok or resp == nil or resp.status ~= "00000000" then
        ngx.log(ngx.ERR, "no permission")
        local ret = {}
        ngx.header["Content-Type"] = "application/json"
        ret.status = "00000003"
        ret.msg = "url no permission"
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.say(cjson.encode(ret))
        ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end
end

-- 待验证cookie内容
local session = common.get_session()
if session == nil then
    ngx.log(ngx.ERR, "invalid cookie")
    local resp = {}
    ngx.header["Content-Type"] = "application/json"
    resp.status = "00000003"
    resp.msg = "login"
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.say(cjson.encode(resp))
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end


get_permission(session)