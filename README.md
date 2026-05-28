# GitHubWall

自动填充 GitHub 贡献热力图的工具。

## 功能

- 支持预设图案（心形、笑脸、菱形等）
- 支持自定义图案（JSON 文件）
- 支持随机填充
- CLI 和 Web 界面

## 安装

```bash
pip install -e ".[dev]"
```

## 使用

### CLI

```bash
# 使用预设图案
githubwall create --repo ./my-wall --pattern heart --year 2024

# 随机填充
githubwall create --repo ./my-wall --random --density 0.5

# 推送到 GitHub
githubwall push --repo ./my-wall --remote origin
```

### Web 界面

```bash
githubwall web
```

然后访问 http://localhost:8000

## 图案格式

```json
{
  "name": "pattern_name",
  "width": 52,
  "height": 7,
  "data": [[0,1,2,3,4,...], ...]
}
```

值说明：
- 0: 无提交
- 1: 低密度
- 2: 中低密度
- 3: 中高密度
- 4: 高密度

## 开发

```bash
# 运行测试
pytest tests/ -v

# 安装开发依赖
pip install -e ".[dev]"
```
