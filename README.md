# MX Quant Radar 修复说明

## 本次修复

- Weekly 兼容旧版对象和当前历史数组。当前数组同时包含旧版双市场记录与 `{ update_time, market: "US" | "CN", LONG, SHORT }` 记录。
- 按时间分别选取美股、中国市场最新一条记录；空数组表示该次没有信号，不沿用旧信号。两市场独立显示更新时间。
- 日线时间与当前表格来自同一份 JSON；自动刷新同时刷新数据和时间。切换标签后，旧请求不会覆盖当前标签。
- 历史矩阵一次性渲染，避免重复解析整个矩阵造成卡顿。
- 登录失效、格式错误、缺失文件和超时显示具体原因。

## 为什么 GitHub 更新了，网页仍可能显示旧数据

GitHub 接收提交后，Cloudflare Pages 还需要成功构建、发布该提交。

本次压缩包的 `history_1d.json` 为 28,914,429 字节（27.57 MiB），`history_1d_china.json` 为 30,556,168 字节（29.14 MiB）。两者都超过 [Cloudflare Pages 的 25 MiB 单文件限制](https://developers.cloudflare.com/pages/platform/limits/)。如果直接发布仓库根目录，这批文件会超限。是否正是此前部署失败的原因，需在项目 Deployments 的失败日志中确认，不能只看 GitHub 文件更新时间判断发布成功。

构建脚本保留仓库中的所有原始 JSON，在 `dist/` 中生成压缩排版的发布副本。历史副本只包含按时间排序的最近 40 期，和网页原本显示的 40 期一致。每日新提交都会重新生成，不需要手动裁剪历史。

## Cloudflare Pages 必须调整的设置

1. 把修复后的 `index.html`、`scripts/build-pages.cjs`、`_headers`、`.gitignore` 上传到现有 GitHub 仓库的 `main` 分支。README 可一并上传。**保留 GitHub 当前的 JSON，不要用下载包中的较早快照覆盖后续新数据。**
2. 在现有 Cloudflare Pages 项目的构建设置中填写：

   | 设置 | 值 |
   | --- | --- |
   | Framework preset | None |
   | Build command | `node scripts/build-pages.cjs` |
   | Build output directory | `dist` |
   | Root directory | 仓库根目录 |
   | Production branch | `main` |

3. 对最新提交重新部署，确认 Deployment 显示 Success，且构建日志输出 `Build complete. Publish dist/`。
4. 打开 mxentropy.com 刷新，验证三个标签的数据时间和 Weekly 的两市场时间。若仍旧，先核对该域名对应的生产部署、提交 SHA，再检查是否有自定义缓存规则覆盖源站缓存设置。

仅替换 HTML 能修复 Weekly 解析，但不能解决大文件导致的发布失败。`dist/` 是发布目录，不需要提交到 GitHub。

## 与现有每日程序配合

现有程序继续向原 JSON 追加记录并推送 GitHub，无需改成写 `dist/`。Cloudflare 对同一次提交中的文件运行构建，自动更新网页副本。`.gitignore` 已忽略 `dist/`，因此正常的 `git add .` 不会把本地生成目录再提交；若以前已经跟踪过 `dist/`，需要单独处理已跟踪状态。

如果多个程序可能同时操作同一文件或同一 Git 目录，写入、commit、push 应串行执行（统一调度或使用共享锁）。此压缩包没有那些每日生成程序，本次未修改它们。源文件长远应按月或按年归档，避免无限增长：GitHub 常规 Git 推送对超过 50 MiB 的单文件警告，并拒绝超过 100 MiB 的文件；网页上传还有单独的 25 MiB 限制，见 [GitHub 官方说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。这与 Cloudflare Pages 的发布限制是两回事。

仓库原有的 `push_index.bat` 固定切换到 `F:\mx_radar_web`，仅适合那个目录确实是目标 Git 仓库时使用。本次未执行批处理、回滚脚本或 Git 推送。

## 下载快照的核对值

以下是用户于 2026-09-30 提供的压缩包中的真实值，并非固定写入页面：

| 数据 | 更新时间 | 其他信息 |
| --- | --- | --- |
| 1D Macro | 2026-09-29 10:51:13 | 与对应历史最后一期一致 |
| 1D China | 2026-09-30 01:29:58 | 与对应历史最后一期一致 |
| Weekly 美股 | 2026-09-29 20:45:20 | LONG 28 / SHORT 36 |
| Weekly 中国 | 2026-09-29 20:42:36 | LONG 28 / SHORT 20 |

原数据没有时区标注，页面保留原文，不擅自加减时差或替换成电脑当前时间。

## 本地预览

在仓库根目录运行：

```text
node scripts/build-pages.cjs
python -m http.server 8000 --directory dist --bind 127.0.0.1
```

然后打开 `http://127.0.0.1:8000/`。不要通过双击 HTML 的 `file://` 地址测试 JSON 加载。

完整源码包保留全部历史；单独的 Pages 发布包只包含 `dist/` 的内容。本次只完成本地修改和验证，未修改 GitHub 或 Cloudflare 的线上设置。
