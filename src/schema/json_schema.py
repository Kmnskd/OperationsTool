ldap_schema = {
  "type": "object",
  "properties": {
      "cn": {
        "description": "姓名",
        "type": "string"
      },
      "uid": {
        "description": "用户名",
        "type": "string"
      },
      "employeeNumber": {
        "description": "工号",
        "type": "string"
      },
      "mail": {
        "description": "邮箱",
        "type": "string",
        "pattern": "^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
      },
      "telephonenumber": {
        "description": "电话号",
        "type": "string"
      },
  },
  "required": ["cn", "uid", "employeeNumber", "mail", "telephonenumber"]
}

