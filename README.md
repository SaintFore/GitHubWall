# GitHubWall

自动填充 GitHub 贡献热力图的工具。

## 工作原理

GitHub 贡献热力图基于 git commit 的日期显示绿色方块。本工具通过在本地仓库中创建指定日期的 commit 来填充热力图。你需要一个专门的 GitHub 仓库来存放这些 commit。

## 前置条件

- Python 3.8+
- Git（已配置 user.name 和 user.email）
- GitHub 账户

## 安装

```bash
git clone <本项目地址>
cd GitHubWall
uv sync
```

## 完整使用流程

### 第一步：在 GitHub 创建空仓库

1. 登录 GitHub，点击右上角 "+" -> "New repository"
2. 仓库名建议用 `githubwall` 或其他你喜欢的名字
3. **不要**勾选 "Add a README file"（保持仓库为空）
4. 点击 "Create repository"
5. 复制仓库地址（SSH 或 HTTPS）

### 第二步：生成 commit

#### 方式一：使用 CLI

```bash
# 使用预设心形图案，填充 2024 年
uv run githubwall create --repo ./my-wall --pattern heart --year 2024

# 使用随机图案，填充 2024 年
uv run githubwall create --repo ./my-wall --random --density 0.5 --year 2024

# 使用自定义日期范围
uv run githubwall create --repo ./my-wall --pattern diamond --start 2024-01-01 --end 2024-06-30

# 可用的预设图案：heart, smile, diamond
```

#### 方式二：使用 Web 界面

```bash
uv run githubwall web
```

然后在浏览器中访问 http://localhost:8000：
1. 在网格上绘制图案，或选择预设图案
2. 设置仓库路径（如 `./my-wall`）
3. 设置日期范围
4. 点击"执行"

### 第三步：推送到 GitHub

```bash
# 添加远程仓库（替换为你的仓库地址）
cd my-wall
git remote add origin git@github.com:你的用户名/githubwall.git

# 推送
uv run githubwall push --repo ./my-wall --remote origin
```

### 第四步：查看热力图

打开你的 GitHub 个人主页，等待几分钟后即可看到热力图变化。

## CLI 命令参考

### `create` - 生成 commit

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--repo` | 仓库路径 | 当前目录 |
| `--pattern` | 预设图案名或 JSON 文件路径 | heart |
| `--random` | 使用随机图案 | false |
| `--density` | 随机密度 (0.0-1.0) | 0.5 |
| `--year` | 目标年份 | 当前年 |
| `--start` | 开始日期 (YYYY-MM-DD) | - |
| `--end` | 结束日期 (YYYY-MM-DD) | - |

### `push` - 推送到远程

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--repo` | 仓库路径 | 当前目录 |
| `--remote` | 远程名称 | origin |

### `web` - 启动 Web 界面

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | 监听地址 | 0.0.0.0 |
| `--port` | 监听端口 | 8000 |

## 图案格式

自定义图案使用 JSON 格式：

```json
{
  "name": "my_pattern",
  "width": 7,
  "height": 7,
  "data": [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 1, 0],
    [1, 2, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 2, 1],
    [0, 1, 2, 2, 2, 1, 0],
    [0, 0, 1, 1, 1, 0, 0]
  ]
}
```

- `width`: 图案宽度（周数，最多 52）
- `height`: 必须为 7（一周 7 天）
- `data`: 二维数组，值 0-4 对应热力图的绿色深浅
  - 0: 无提交（灰色）
  - 1: 浅绿
  - 2: 中绿
  - 3: 深绿
  - 4: 最深绿

## 常见问题

**Q: 热力图没有显示？**
A: GitHub 热力图更新可能需要几分钟。确保 commit 的 email 与 GitHub 账户一致。

**Q: 可以用已有的仓库吗？**
A: 建议创建专用仓库。如果用已有仓库，`create` 命令会重新 `git init`，覆盖原有历史。

**Q: 如何只填充部分时间段？**
A: 使用 `--start` 和 `--end` 参数指定日期范围。

## 开发

```bash
# 安装依赖
uv sync

# 运行测试
uv run pytest tests/ -v
```
