# GitHubWall

自动填充 GitHub 贡献热力图的工具。

## 为什么要有这个项目

谁不想让自己的 GitHub 热力图一片绿呢？但现实是，我们不可能每天都有代码要提交。于是为了凑数，只能反复改改 dotfiles 配置然后 push——说实话，这挺没意思的。

所以这个项目诞生了：与其手动凑数，不如让工具帮你搞定。省下来的时间，去做点真正有趣的事。

## 工作原理

GitHub 热力图根据 commit 日期显示绿色方块。本工具通过设置 `GIT_AUTHOR_DATE` 和 `GIT_COMMITTER_DATE` 环境变量，在本地仓库中创建指定日期的 commit，然后推送到 GitHub 即可。建议使用一个专用仓库来存放这些 commit。

## 前置条件

- Python 3.8+
- Git（已配置 user.name 和 user.email）
- GitHub 账户

## 安装

```bash
git clone https://github.com/SaintFore/GitHubWall.git
cd GitHubWall
uv sync
```

## 完整使用流程

### 第一步：在 GitHub 创建空仓库

1. 登录 GitHub，点击右上角 "+" -> "New repository"
2. 仓库名随意，比如 `wall` 或 `contributions`
3. **不要**勾选 "Add a README file"，保持仓库为空
4. 点击 "Create repository"，复制仓库地址

### 第二步：生成 commit

#### 方式一：CLI 命令行

```bash
# 涂满整年，随机深浅（最自然的方式）
uv run githubwall create --repo ./my-wall --fill --vary --year 2024

# 涂满整年，固定级别（1-4，颜色均匀）
uv run githubwall create --repo ./my-wall --fill --level 3 --year 2024

# 涂满整年，全部最深色
uv run githubwall create --repo ./my-wall --fill --level 4 --year 2024

# 预设图案：heart（心形）、smile（笑脸）、diamond（菱形）
uv run githubwall create --repo ./my-wall --pattern heart --year 2024

# 随机图案，可调节密度（0.0-1.0）
uv run githubwall create --repo ./my-wall --random --density 0.6 --year 2024

# 自定义日期范围
uv run githubwall create --repo ./my-wall --pattern diamond --start 2024-01-01 --end 2024-06-30
```

#### 追加多年份

可以在同一个仓库中追加不同年份，不会覆盖已有提交：

```bash
uv run githubwall create --repo ./my-wall --fill --vary --year 2024
uv run githubwall create --repo ./my-wall --fill --vary --year 2025
```

#### 方式二：Web 界面

```bash
uv run githubwall web
```

浏览器打开 http://localhost:8000，可以可视化绘制图案、选择预设、设置日期范围后一键执行。

### 第三步：推送到 GitHub

```bash
cd my-wall
git remote add origin git@github.com:你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

### 第四步：查看热力图

打开你的 GitHub 个人主页，等待几分钟后即可看到热力图变化。

## 自动保持热力图活跃（GitHub Actions）

手动填充只能搞定过去的年份。想让以后的热力图也保持绿色，可以用 GitHub Actions 每天自动提交一个 commit。

### 第一步：生成 workflow 文件

```bash
uv run githubwall workflow --repo ./my-wall
```

会在 `./my-wall/.github/workflows/` 下生成 `daily-commit.yml`。

### 第二步：创建 Personal Access Token

1. GitHub -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens
2. 点击 "Generate new token"
3. Token name 随意，比如 `githubwall-daily`
4. Repository access 选择你创建的目标仓库
5. Permissions -> Contents: Read and write
6. 生成并复制 token

### 第三步：添加 Secret

1. 打开目标仓库 -> Settings -> Secrets and variables -> Actions
2. New repository secret，名称填 `PAT`，值粘贴上一步的 token

### 第四步：推送并启用

```bash
cd my-wall
git add .
git commit -m "chore: add daily commit workflow"
git push
```

在仓库的 Actions 页面启用 workflow。之后每天北京时间 20:00 会自动运行，也可以手动触发。

## CLI 命令参考

### `create` - 生成 commit

| 参数        | 说明                        | 默认值   |
| ----------- | --------------------------- | -------- |
| `--repo`    | 仓库路径                    | 当前目录 |
| `--pattern` | 预设图案名或 JSON 文件路径  | heart    |
| `--random`  | 使用随机图案                | false    |
| `--density` | 随机密度 (0.0-1.0)          | 0.5      |
| `--fill`    | 涂满模式（每天都有 commit） | false    |
| `--level`   | 涂满模式的固定级别 (1-4)    | 2        |
| `--vary`    | 涂满模式随机变化级别        | false    |
| `--year`    | 目标年份                    | 当前年   |
| `--start`   | 开始日期 (YYYY-MM-DD)       | -        |
| `--end`     | 结束日期 (YYYY-MM-DD)       | -        |

### `push` - 推送到远程

| 参数       | 说明     | 默认值   |
| ---------- | -------- | -------- |
| `--repo`   | 仓库路径 | 当前目录 |
| `--remote` | 远程名称 | origin   |

### `web` - 启动 Web 界面

| 参数     | 说明     | 默认值  |
| -------- | -------- | ------- |
| `--host` | 监听地址 | 0.0.0.0 |
| `--port` | 监听端口 | 8000    |

### `workflow` - 生成 GitHub Actions workflow

| 参数     | 说明         | 默认值   |
| -------- | ------------ | -------- |
| `--repo` | 目标仓库路径 | 当前目录 |

## 自定义图案

支持 JSON 格式的自定义图案。高度固定为 7（一周 7 天），宽度最大 52（一年 52 周）：

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

值的含义对应热力图绿色深浅：

| 值 | 颜色 | 对应 commit 数 |
|----|------|---------------|
| 0  | 灰色 | 0 |
| 1  | 浅绿 | 1 |
| 2  | 中绿 | 3 |
| 3  | 深绿 | 5 |
| 4  | 最深 | 10 |

## 常见问题

**Q: 热力图没有显示？**
A: GitHub 更新可能需要几分钟到几小时。另外确保 commit 的 email 与 GitHub 账户一致（用 `git config user.email` 检查）。

**Q: 可以用已有的仓库吗？**
A: 建议用新仓库。`create` 会执行 `git init`，会覆盖原有 git 历史。

**Q: 如何只填充部分时间段？**
A: 用 `--start` 和 `--end` 指定日期范围，比如 `--start 2024-03-01 --end 2024-06-30`。

**Q: 多个年份怎么处理？**
A: 在同一个仓库里多次执行 `create` 即可，提交会追加不会覆盖。

**Q: 能撤销吗？**
A: 删除仓库重新生成即可。推送后无法远程撤销已显示的热力图。

## 开发

```bash
git clone <本项目地址>
cd GitHubWall
uv sync               # 安装依赖
uv run pytest tests/ -v  # 运行测试
```
