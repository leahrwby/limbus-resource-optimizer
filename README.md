# Limbus Resource Optimizer

一个用于优化《Limbus Company》资源分配的 Codex Skill。

它可以根据玩家当前拥有的体力、脑啡肽模块、体力盒、狂气和通行证进度，计算每日换多少次体力更合适，以及能够获得多少通行证等级、人格碎片箱和期望人格碎片。

> 本项目是玩家制作的非官方工具，与 Project Moon 无关。

## 主要功能

- 计算自然恢复产生的体力
- 计算体力可以转换成多少脑啡肽模块
- 计算每日狂气换体的阶梯成本
- 比较不同每日换体次数的收益
- 计算普通镜牢可刷次数
- 计算获得的通行证经验和等级
- 计算通行证120级后获得的人格碎片箱
- 区分免费通行证与付费通行证收益
- 估算人格碎片箱的期望碎片数量
- 保留指定数量的狂气，避免过度消耗
- 将抽卡所需狂气作为机会成本进行比较

## 支持的输入

计算时可以提供：

- 计划持续天数
- 当前体力上限
- 当前体力
- 当前脑啡肽模块数量
- 当前体力盒数量
- 当前狂气数量
- 希望保留的最低狂气
- 是否购买付费通行证
- 距离通行证120级所需经验
- 当前EX等级经验进度
- 计划领取的镜牢周常奖励次数
- 每天预留给经验本、纺锤本等内容的模块
- 最多有时间完成多少次镜牢
- 自然恢复体力的实际利用率

## 使用示例

假设：

- 计算未来30天
- 体力上限为150
- 当前拥有6500狂气
- 至少保留2600狂气
- 已购买付费通行证
- 通行证已经达到120级
- 期间可以领取12次普通镜牢周常奖励

运行：

```bash
python scripts/optimize_resources.py \
  --days 30 \
  --enkephalin-cap 150 \
  --lunacy 6500 \
  --lunacy-reserve 2600 \
  --paid-pass \
  --xp-to-pass-cap 0 \
  --weekly-bonus-claims 12
```

在 Windows PowerShell 中也可以写成一行：

```powershell
python scripts/optimize_resources.py --days 30 --enkephalin-cap 150 --lunacy 6500 --lunacy-reserve 2600 --paid-pass --xp-to-pass-cap 0 --weekly-bonus-claims 12
```

输出内容包括：

- 推荐的总换体次数
- 每天应该换多少次体力
- 消耗和获得的狂气
- 可生成的脑啡肽模块
- 可完成的普通镜牢次数
- 获得的通行证经验
- 获得的EX等级
- 获得的人格碎片箱
- 期望人格碎片
- 计算结束后的剩余资源
- 收益相近的替代方案

## 安装为 Codex Skill

将仓库克隆或下载到 Codex Skills 目录：

```bash
git clone https://github.com/YOUR_USERNAME/limbus-resource-optimizer.git
```

也可以下载仓库 ZIP，解压后把整个 `limbus-resource-optimizer` 文件夹放入 Codex 的 Skills 目录。

安装后可以这样提问：

```text
使用 $limbus-resource-optimizer 帮我计算每天换几次体力最划算。
```

或者：

```text
我有5000狂气，体力上限150，已经购买通行证并达到120级。
未来30天至少保留2600狂气，每天最多打3次普牢，应该怎样安排换体？
```

## 当前采用的主要规则

当前数据快照更新于2026年8月3日。

- 每6分钟自然恢复1点体力
- 每天最多自然恢复240点体力
- 20点体力可以转换为1个脑啡肽模块
- 1个体力盒恢复60点体力
- 每日第 `n` 次狂气换体消耗 `26 × n` 狂气
- 每日最多使用狂气换体10次
- 每次换体恢复等同于当前体力上限的体力
- 普通镜牢完整领取奖励消耗5个模块
- 无周常加成的普通镜牢提供30点通行证经验
- 使用一次周常加成时提供45点通行证经验和250免费狂气
- 每10点经验提升1级通行证
- 通行证120级后，免费轨道每级获得1个自选人格碎片箱
- 付费通行证每级合计获得3个自选人格碎片箱
- 每个自选人格碎片箱提供1～3片指定罪人的人格碎片
- 计算器采用每箱2片作为长期数学期望

具体数据、来源与更新时间见：

- `references/game-data.md`
- `references/game-data.json`

## 计算范围与限制

当前优化目标是：

> 在给定狂气、体力、模块、时间和储备要求的情况下，最大化通过普通镜牢获得的自选人格碎片箱。

目前没有统一计算以下内容的价值：

- 困难镜牢的不同周常领取方式
- 限时活动商店
- 经验票和纺锤收益
- 主线与活动关卡的首次奖励
- 维护补偿
- 玩家实际完成镜牢所需时间
- 抽取限定人格或E.G.O的战略价值
- 娱乐体验和重复刷取疲劳

因此，“箱子数量最大化”不一定等于“账号整体价值最大化”。计算结果应作为资源规划参考，而不是唯一正确的游玩方式。

## 数据来源

主要参考：

- [Enkephalin](https://limbuscompany.wiki.gg/wiki/Enkephalin)
- [Lunacy](https://limbuscompany.wiki.gg/wiki/Lunacy)
- [Mirror Dungeons](https://limbuscompany.wiki.gg/wiki/Mirror_Dungeons)
- [Limbus Pass](https://limbuscompany.wiki.gg/wiki/Limbus_Pass)
- [Egoshard](https://limbuscompany.wiki.gg/wiki/Egoshard)
- [Dispenser](https://limbuscompany.wiki.gg/wiki/Dispenser)

游戏规则可能随版本更新而变化。如果发现数据已经调整，欢迎提交 Issue 或 Pull Request。

## 反馈与联系

如果你发现游戏数据已经过时、计算结果存在错误，或者希望建议新功能，可以通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至：2581818406@qq.com

反馈时建议附上游戏版本、相关截图、数据来源以及计算参数，方便核验和修正。

## License

本项目使用 MIT License。

《Limbus Company》及其相关名称、设定与游戏内容的权利归 Project Moon 所有。
