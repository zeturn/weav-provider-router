# Quick Setup Guide for PyPI Publishing

## 🚀 在 5 分钟内设置自动发布

### 1️⃣ 在 PyPI 上配置 Trusted Publisher（首次设置）

访问：https://pypi.org/manage/account/publishing/

添加待发布项目：
```
项目名称: weav-provider-router
GitHub 用户名/组织: HungryZhao
仓库名称: weav-provider-router-repo
工作流文件: publish.yml
环境名称: pypi
```

### 2️⃣ 在 GitHub 上创建环境

1. 进入仓库 Settings → Environments
2. 点击 "New environment"
3. 名称: `pypi`
4. （可选）添加保护规则

### 3️⃣ 发布新版本

#### 方法 A: 使用版本管理脚本（推荐）

```bash
# 安装到当前环境（如果需要）
cd weav-provider-router-repo

# 补丁版本（0.1.0 → 0.1.1）
python scripts/bump_version.py patch

# 次要版本（0.1.0 → 0.2.0）
python scripts/bump_version.py minor

# 主要版本（0.1.0 → 1.0.0）
python scripts/bump_version.py major

# 推送更改和标签
git push
git push origin v0.1.1  # 替换为实际版本
```

#### 方法 B: 手动发布

```bash
# 1. 更新版本号
# 编辑 pyproject.toml，修改 version = "0.1.1"

# 2. 提交更改
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.1.1"

# 3. 创建标签
git tag v0.1.1
git push origin master
git push origin v0.1.1

# 4. 在 GitHub 上创建 Release
# 访问: https://github.com/HungryZhao/weav-provider-router-repo/releases/new
# 选择标签 v0.1.1，填写发布说明，点击 "Publish release"
```

### 4️⃣ 验证发布

发布后检查：
- ✅ GitHub Actions 工作流运行成功
- ✅ PyPI 上的包页面：https://pypi.org/project/weav-provider-router/
- ✅ 安装测试：`pip install weav-provider-router`

---

## 🧪 测试发布流程（使用 TestPyPI）

在正式发布前，先在 TestPyPI 上测试：

### 1. 在 TestPyPI 上配置

访问：https://test.pypi.org/manage/account/publishing/

添加相同配置，但环境名称使用 `testpypi`

### 2. 创建 TestPyPI 环境

在 GitHub Settings → Environments 创建 `testpypi` 环境

### 3. 手动触发测试发布

1. 进入 GitHub Actions
2. 选择 "Publish to PyPI" 工作流
3. 点击 "Run workflow"
4. 这将发布到 TestPyPI

### 4. 从 TestPyPI 安装测试

```bash
pip install --index-url https://test.pypi.org/simple/ weav-provider-router
```

---

## 📋 发布前检查清单

- [ ] 所有测试通过
- [ ] 版本号已更新
- [ ] CHANGELOG.md 已更新
- [ ] README.md 最新
- [ ] 本地构建成功：`python -m build`
- [ ] 包检查通过：`twine check dist/*`
- [ ] PyPI Trusted Publisher 已配置
- [ ] GitHub 环境已创建

---

## 🔧 常用命令

```bash
# 本地构建测试
python -m build
twine check dist/*

# 查看当前版本
grep "version =" pyproject.toml

# 查看所有标签
git tag -l

# 删除标签（如果需要）
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0

# 查看工作流状态
gh workflow view publish.yml  # 需要 GitHub CLI
```

---

## ❓ 常见问题

**Q: 发布失败，提示 "Trusted publisher not configured"**  
A: 需要先在 PyPI 上配置 Trusted Publisher（步骤 1）

**Q: 如何回滚版本？**  
A: 不能删除 PyPI 上的版本，只能发布新版本修复问题

**Q: 可以重新上传相同版本吗？**  
A: 不可以。必须使用新版本号

**Q: 如何撤回错误的发布？**  
A: 可以在 PyPI 上 "yank" 版本（标记为不推荐），但不能删除

---

## 📚 详细文档

查看 [PUBLISHING.md](PUBLISHING.md) 了解完整的发布指南和故障排除。

---

**首次发布后，所有后续版本只需创建 GitHub Release 即可自动发布！** 🎉
