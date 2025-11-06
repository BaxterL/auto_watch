# 介绍

本项目是重庆高等智慧教育平台自动刷课，只能刷课程和文档，评论和题目要自己做。

# 说明

最开始想用request写方便点，结果发现我写起来一点都不方便，不如直接做自动化吧...推荐去上课的时候电脑挂一个这个。修改脚本的`username`和`password`为你自己的账号密码。`maxworks`控制最大窗口数，你可以多个同时进行，本项目也是为此开发的

# 部署

项目需要chromedriver [下载链接](https://developer.chrome.google.cn/docs/chromedriver/downloads?hl=zh-cn)

```bash
#Need Python 3.14+
pip install -r requirements.txt
```

# 运行

```bash
python a.py
```