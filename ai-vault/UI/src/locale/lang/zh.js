export default {
  // Header
  PLATFORM_TITLE: 'AIVault',
  MINDX_TITLE: 'MindX',
  LOGIN_WELCOME: '欢迎到访',
  CHANGE_PASSWORD: '修改密码',
  LOGOUT: '退出',
  VERSION: '版本',
  HEALTH_STATUS: '健康状态',
  USER_AMOUNT: '用户总数',
  TOOL_INFO: '组件信息',
  SYS_DATA_SIZE: '系统数据大小（MB）',
  CERT_INFO: '组件证书',

  // Sider
  NAV_HOME: '首页',
  NAV_USER: '用户管理',
  NAV_AI_VAULT: '密钥管理',

  // Tabs
  TAB_MAIN_KEY: '主密钥',
  TAB_PRE_KEY: '预共享密钥',

  PLACEHOLDER_INPUT: '请输入名称查询 ...',
  BUTTON_ADD: '新增密钥',
  BUTTON_CERT: '申请证书',
  BUTTON_ADD_USER: '新增用户',
  BUTTON_UPLOAD: '上传数据',
  BUTTON_DOWNLOAD: '下载数据',

  // 表格列名
  COLUMN_NAME: '名称',
  COLUMN_CREATE_TYPE: '创建类型',
  COLUMN_KEY_USAGE: '密钥用途',
  COLUMN_CREATE_TIME: '创建时间',
  COLUMN_REMARKS: '备注',
  COLUMN_OPERATION: '操作',
  COLUMN_BIND_MK_NAME: '绑定的主密钥名称',
  COLUMN_CERT_TYPE: '证书类型',
  COLUMN_CERT_VALID_DATE: '证书有效期',
  COLUMN_CERT_ALARM: '证书告警',
  COLUMN_CRL_STATUS: '吊销列表状态',
  COLUMN_USER_ID: '用户id',
  COLUMN_USER_NAME: '用户名',
  COLUMN_USER_TYPE: '用户类型',
  FILTER_VALID: '有效',
  FILTER_INVALID: '无效',
  OPERATION_DELETE: '删除',
  EMPTY_TEXT: '暂无数据',
  RESET_PASSWORD: '重置密码',
  UPLOAD_RISK: '上传提示',

  //表单
  PLACEHOLDER_USERNAME: '请输入用户名',
  PLACEHOLDER_PASSWORD: '请输入密码',
  PLACEHOLDER_CURRENT_PASSWORD: '请输入账号密码',
  PLACEHOLDER_NEW_PASSWORD: '请输入新密码',
  PLACEHOLDER_CONFIRM_PASSWORD: '请再次输入新密码',
  PLACEHOLDER_KEY_NAME: '请输入密钥名称',
  PLACEHOLDER_KEY_USAGE: '请输入密钥用途',
  PLACEHOLDER_COMMENT: '请输入相关描述',
  PLACEHOLDER_PSK_NAME: '请输入预共享密钥名称',
  PLACEHOLDER_MK_NAME: '请输入主密钥名称',
  PLACEHOLDER_MK_PASSWORD: '请输入口令',
  PLACEHOLDER_KEY_PASSWORD: '请输入用户持有的口令',
  PLACEHOLDER_CERT_COMMONNAME:'请输入公共名字',
  PLACEHOLDER_CERT_KEYWORD:'请输入加密私钥密码',
  PLACEHOLDER_CERT_ORGANIZATION:'请输入组织',
  PLACEHOLDER_CERT_UNIT:'请输入二级组织名',
  PLACEHOLDER_CERT_COUNTRY:'请输入国家',
  PLACEHOLDER_CERT_PROVINCE:'请输入省',
  PLACEHOLDER_CERT_CITY:'请输入市',
  CERT_COMMONNAME:'公用名',
  CFS_PASSWORD:'加密私钥密码',
  CERT_ORGANIZATION_NAME:'组织名',
  CERT_UNIT_NAME:'二级组织名',
  CERT_LOCATION:'地区名字',
  SUBMIT: '提交',
  LOGIN: '登录',
  CURRENT_PSW: '当前密码',
  NEW_PSW: '新密码',
  CONFIRM_PSW: '确认密码',
  ERR_SAME_CURRENT_PASSWORD: '不能与当前密码相同',
  ERR_CANNOT_CONFIRM_NEW_PASSWORD: '两次输入的密码不一致',
  KEY_NAME: '密钥名称',
  KEY_USAGE: '密钥用途',
  PSK_NAME: '预共享密钥名',
  MK_NAME: '主密钥名',
  USER_PASSWORD: '口令',
  COMMENT: '备注',
  BASIC_INFO: '基础信息',
  BTN_OK: '确定',
  BTN_CANCEL: '取消',
  BTN_COPY: "复制到剪贴板",
  CONFIRM_DELETE: '删除提醒',
  CONFIRM_DELETE_TIP: '请确认是否要删除',
  CONFIRM_DELETE_KEY_TIP: '删除后将无法加解密模型。',
  CONFIRM_UPLOAD_TIP: '上传文件会覆盖相同命名文件，并重启进程。请确认是否要进行此操作？',

  // Message
  ERR_LOGIN: '用户名或密码错误',
  ERR_LOGIN_LOCKING: '多次输入账户或密码错误，请稍后重试',
  SUCCESS_LOGIN: '登录成功',
  SUCCESS_ADD: '添加成功，请妥善保管主密钥，关闭窗口后将无法查询得到！',
  SUCCESS_APPLY: '证书配置完成，正在自动下载，请留意浏览器下载进度',
  SUCCESS_UPLOAD: '上传成功',
  ERR_UPLOAD: '上传失败',
  ERR_DOWNLOAD: '下载数据失败',
  SUCCESS_DELETE: '删除成功',
  ERR_DELETE: '删除失败',
  ERR_DELETE_MK: '该密钥已绑定预共享密钥，请删除对应预共享密钥后重试。',
  ERR_DELETE_USER: '该用户存在正在使用的主密钥，请删除密钥后重试。',
  ERR_CONNECT_AIVAULT: '无法确认用户密钥状况，请开启AIVAULT服务后重试。',
  ERR_ADD_MK: '该主密钥已存在',
  ERR_ADD_PSK: '该预共享密钥已存在',
  ERR_MK_AREADY_BIND: '所填主密钥已绑定',
  ERR_ADD_PSK_MK_NOT_EXIST: '所填主密钥不存在',
  SUCCESS_OPERATION: '操作成功',
  ERR_OPERATION: '操作失败',
  SUCCESS_CHANGE_PASSWORD: '修改密码成功',
  ERR_CHANGE_PASSWORD: '修改密码失败',
  SUCCESS_RESET_PASSWORD: '重置密码成功',
  ERR_RESET_PASSWORD: '修改密码失败',
  SUCCESS_ADD_USER: '添加用户成功',
  ERR_ADD_USER: '添加用户失败',
  ERR_USER_NUM_EXCEED: '用户数量已满500，添加用户失败',
  SUCCESS_COPY: '复制成功',
  ERR_COPY: '复制失败',
  ERR_ADD: '添加失败',
  ERR_USER_AREADY_EXIST: '该用户名已存在',
  ERR_PARAMS_CHECK_FAILED: '参数格式不符合要求',
  ERR_NOT_MEET_PASSWORD_COMPLEXY: '该口令不符合复杂度要求',
  ERR_UPLOAD_FILE_SIZE: '上传文件大小不能超过 50MB!',
  ERR_UPLOAD_FILE_TYPE: '上传文件必须为 zip 格式',
  ERR_MAX_MK: '主密密钥量超过上限',
  ERR_MAX_PSK: '预共享密钥数量超过上限',
  ERR_SYSTEM_BUSY: '系统繁忙，请稍后重试',


  DIALOG_COPY: '请确认是否要将预共享密钥复制到剪切板：',
  PSK_TIP: '请妥善保管预共享密钥，关闭窗口后将无法查询得到！',
  PSK_TITLE: '预共享密钥',
  PSK_TIPS: '关闭弹窗将无法再次获取预共享密钥，请妥善保管预共享密钥。您可以选择将预共享密钥复制到剪贴板',
  ADD_MK: '新建主密钥',
  ADD_PSK: '新建预共享密钥',
  ADD_CERT: '申请CFS证书',
  ADD_MK_TIP: '新建成功后将自动下载主密钥，请妥善保管主密钥，主密钥丢失将无法找回',
  ADD_PSK_TIP: '主密钥与预共享密钥一一对应。新建完成将自动下载预共享密钥，请留意保存',
  ADD_CERT_TIP: '配置完成将自动下载证书，系统无法保存证书配置信息，证书丢失需要重新下载',
  ADD_USER_TIP: '用户总数最多为500',

  // Tooltip
  TIP_ADD_USER_USERNAME: '长度为[1, 32]，仅支持数字、字母、下划线和”-“字符。必须以字母开头。',
  TIP_PASSWORD: '长度为[8, 20]，仅支持数字、字母、英文特殊字符（至少包含两种）。',
  TIP_KEY_NAME: '长度为[1, 128]，仅支持数字、字母、下划线和”-“字符。',
  TIP_KEY_USAGE: '长度为[1, 128]，仅支持数字、字母、空格、下划线和”-“字符，不支持全空格。',
  TIP_KEY_PASSWORD: '长度为[40, 64]，仅支持数字、字母、英文特殊字符（至少包含两种），且不能与密钥名称或反转密钥名称相同。',
  TIP_REMARKS: '仅支持数字、字母、空格、下划线和和”-“字符。',
  TIP_LOCATION:'长度在2以下，仅支持字母',
  TIP_COMMON:'长度在64以下，仅支持字母',

};
