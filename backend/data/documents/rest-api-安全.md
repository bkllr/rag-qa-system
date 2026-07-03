# REST API 安全

## 常见威胁
- SQL注入: 使用参数化查询防护
- XSS: 转义输出 + CSP头
- CSRF: Token防护
- DDoS: 速率限制

## 最佳实践
- 强制 HTTPS
- API Key / JWT 认证
- 输入验证（永远不信任用户输入）
- 最小权限原则
- 日志记录所有异常访问