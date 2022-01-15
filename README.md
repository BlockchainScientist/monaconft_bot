## monaconft机器人
这是基于Python3实现的monaconft机器人。机器人能自动创建地址，注册/登录，like和follow任意的用户。

**Clone使用代码前麻烦请点击Star收藏，不花钱的，这是我后续更新的动力**，后续可能增加的功能：
1. 批量转账mona给机器人
2. 自动质押mona
3. 后续更严格的人机验证出来后，绕过新版人机验证
4. 实时交互功能，不停机指定用户点赞

后续根据Star数视情况更新。

## 依赖
本项目使用python3 + web3 + selenium实现，所使用Chrome为v96版本，请事先准备好相同环境。

安装python3请百度

web3库在window下需要vc++14以上，请实现安装最新版VisualStudio，然后工具安装C++桌面程序套装即可。然后再安装web3库：

## 安装运行
安装运行前，确保你的当前路径在monaconft_bot文件夹下

安装python包：
```shell
pip install -r requirements.txt
```

生成机器人账号：
```shell
# window
py ./src/gen_address.py
# mac
python3 ./src/gen_address.py
```

在target_uid.txt文件中填写你需要follow和like的账号，注意一行一条


运行程序：
```
py ./src/main.py
```

## 配置说明
在main.py中修改thread_num设置线程数，即可同时打开的浏览器

在main.py中修改rand_follow_num设置随机follow的其他人的账号

## monaconft规则说明
monaconft是一个非常中心化和强势的项目，从上线以来一直在修改规则和封号，如果想玩就做好**被项目方不断修改规则耍猴和被随意封号的准备**。由于项目组的不可确定性，会给投入的资产带来非常大的风险，所以目前已不再继续关注这个项目。下面介绍目前比较稳妥的刷空投的策略。

目前举报会针对高赞和高评论的用户，并且post数还不少(一天发3条手动复制币圈新闻也会大概率被封)，所以建议不要发太多post，让机器人只follow即可。目前只有质押200 mona的用户交互才能算分，所以不仅自己的账号需要质押200 mona，也需要给每个机器人质押200 mona。上面的代码可以自动生成地址，你可以手动转账，也可以利用批量转账工具为每个机器人预备好bnb和mona。建议质押不要太久，因为平台的规则一周变一次，所以你不知道下周到底需要更多船还是更多mona来进行挖矿。

