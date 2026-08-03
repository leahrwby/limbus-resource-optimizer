# Limbus Resource Optimizer

一个用于优化《Limbus Company》资源分配的 Codex Skill。

它可以根据玩家当前拥有的体力、脑啡肽模块、体力盒、免费狂气、付费狂气、月卡、通行证进度和可用时间，计算每日换多少次体力更合适，以及能够获得多少通行证等级、人格碎片箱和期望人格碎片。

> 本项目是玩家制作的非官方工具，与 Project Moon 无关。

## 主要功能

- 计算自然恢复产生的体力及可转换的脑啡肽模块
- 计算每日狂气换体的阶梯成本，并比较不同换体次数的收益
- 分开记录免费狂气与付费狂气，优先使用免费狂气换体
- 保护指定数量的总狂气和付费狂气，避免影响通行证等付费项目
- 计算普通镜牢与困难镜牢的模块、通行证经验和狂气收益
- 比较困难镜牢一次使用三格加成与三次分别使用单格加成
- 自动读取当前日期和星期，计算规划期内可获得的镜牢周加成
- 按韩国时间每周四 06:00（香港及北京时间周四 05:00）计算周刷新
- 默认优先将镜牢周加成用于困难镜牢；明确未解锁困难镜牢时改用普通镜牢
- 支持填写本周已经使用的镜牢周加成数量
- 可选计入普通定期维护补偿；默认参考值为300免费狂气，实际以公告为准
- 计算第7赛季通行证1～120级的固定奖励
- 计算通行证120级后的循环人格碎片箱收益
- 区分免费通行证与付费通行证收益
- 计算大月卡、小月卡带来的免费狂气与付费狂气
- 估算人格碎片箱的期望碎片数量
- 将抽卡所需狂气作为机会成本进行比较

## 支持的输入

计算时可以提供：

- 计划持续天数
- 当前日期、时间和时区；未填写时读取当前时间
- 当前体力上限、体力、脑啡肽模块和体力盒
- 当前免费狂气和付费狂气
- 希望保留的最低总狂气与最低付费狂气
- 大月卡和小月卡在规划期内可领取的天数
- 是否计入新购月卡立即获得的付费狂气
- 是否购买付费通行证
- 当前第7赛季通行证等级及经验进度
- 距离通行证120级所需经验
- 本周已经使用的镜牢周加成数量
- 是否尚未解锁困难镜牢
- 困难镜牢采用一次三加成、三次单加成或自动比较
- 是否计入已公布的维护补偿
- 每天预留给经验本、纺锤本等内容的模块
- 最多有时间完成多少次镜牢
- 自然恢复体力的实际利用率

## 使用示例

假设：

- 计算未来30天
- 体力上限为150
- 当前拥有5000免费狂气和1500付费狂气
- 至少保留2600总狂气，其中至少保留1300付费狂气
- 大月卡和小月卡各可领取30天
- 已购买付费通行证并达到120级
- 本周尚未使用镜牢周加成
- 已解锁困难镜牢，由计算器比较一次三加成与三次单加成

运行：

```bash
python scripts/optimize_resources.py \
  --days 30 \
  --enkephalin-cap 150 \
  --free-lunacy 5000 \
  --paid-lunacy 1500 \
  --lunacy-reserve 2600 \
  --paid-lunacy-reserve 1300 \
  --large-monthly-days 30 \
  --small-monthly-days 30 \
  --paid-pass \
  --xp-to-pass-cap 0 \
  --weekly-bonus-charges-used 0 \
  --hard-weekly-strategy auto
```

在 Windows PowerShell 中也可以写成一行：

```powershell
python scripts/optimize_resources.py --days 30 --enkephalin-cap 150 --free-lunacy 5000 --paid-lunacy 1500 --lunacy-reserve 2600 --paid-lunacy-reserve 1300 --large-monthly-days 30 --small-monthly-days 30 --paid-pass --xp-to-pass-cap 0 --weekly-bonus-charges-used 0 --hard-weekly-strategy auto
```

如果尚未解锁困难镜牢，添加：

```text
--no-hard-unlocked
```

如果要预计一次普通维护的300免费狂气补偿，添加：

```text
--maintenance-compensations 1
```

维护补偿不是固定周收入。如果官方公告给出的金额不同，可使用 `--maintenance-compensation-amount` 修改金额。

输出内容包括：

- 当前星期与下一次镜牢周刷新时间
- 规划期内可使用的镜牢周加成数量
- 推荐的困难镜牢与普通镜牢次数
- 困难镜牢采用一次三加成还是三次单加成
- 推荐的总换体次数与每日换体分布
- 消耗、获得和剩余的免费及付费狂气
- 可生成的脑啡肽模块
- 获得的通行证经验与EX等级
- 获得的人格碎片箱与期望人格碎片
- 收益相近的替代方案

## 查询第7赛季通行证奖励

查询61～80级的免费与付费通行证奖励：

```bash
python scripts/pass_rewards.py --from-level 61 --to-level 80 --paid-pass
```

不填写 `--paid-pass` 时只统计免费轨道。完整的1～120级奖励表位于：

- `references/season-7-pass-rewards.md`
- `references/season-7-pass-rewards.json`

## 安装为 Codex Skill

克隆仓库：

```bash
git clone https://github.com/leahrwby/limbus-resource-optimizer.git
```

也可以点击 GitHub 仓库页面上的 `Code` → `Download ZIP`，解压后把整个 `limbus-resource-optimizer` 文件夹放入 Codex 的 Skills 目录。

安装后可以这样提问：

```text
使用 $limbus-resource-optimizer，根据今天是星期几，帮我计算这周还能刷几次困牢，以及每天换几次体力最划算。
```

或者：

```text
我有5000免费狂气、1500付费狂气，体力上限150，已经购买通行证并达到120级。
未来30天至少保留2600狂气和1300付费狂气，本周还没领取镜牢加成，帮我安排困牢和换体。
```

## 让 Codex 自动安装

复制下面的提示词并发送给 Codex：

> 请从这个 GitHub 仓库安装 Codex Skill：
> https://github.com/leahrwby/limbus-resource-optimizer
>
> 请检查 `SKILL.md` 和目录结构，将其安装到我的 Codex Skills 目录，完成后验证 Skill 能否被正常识别。

## 当前采用的主要规则

当前数据快照更新于2026年8月4日，游戏环境为第7赛季。

- 每6分钟自然恢复1点体力，每天最多自然恢复240点体力
- 20点体力可以转换为1个脑啡肽模块
- 1个体力盒恢复60点体力
- 每日第 `n` 次狂气换体消耗 `26 × n` 狂气，每日最多10次
- 每次换体恢复等同于当前体力上限的体力
- 每周四韩国时间06:00刷新三格镜牢周加成
- 普通镜牢完整领取奖励消耗5个模块
- 无周加成的普通镜牢提供30点通行证经验
- 普通镜牢使用一格周加成时提供45点通行证经验和250免费狂气
- 困难镜牢一次使用三格加成消耗18模块，获得225通行证经验和750免费狂气
- 困难镜牢分三次使用单格加成共消耗18模块，获得250通行证经验和750免费狂气，但需要完成三次困牢
- 每10点经验提升1级通行证
- 第7赛季固定奖励轨道为1～120级
- 通行证120级后，免费轨道每级获得1个自选人格碎片箱
- 付费通行证在120级后每级合计获得3个自选人格碎片箱
- 每个自选人格碎片箱提供1～3片指定罪人的人格碎片，计算器采用每箱2片作为长期数学期望
- 大月卡立即获得650付费狂气，并在30个登录日每天获得65免费狂气
- 小月卡立即获得130付费狂气，并在30个登录日每天获得39免费狂气
- 普通定期维护通常补偿300免费狂气，但不保证每周一定发放，特殊问题的补偿另行计算

具体数据、来源与更新时间见：

- `references/game-data.md`
- `references/game-data.json`
- `references/season-7-pass-rewards.md`
- `references/lunacy-and-monthly-packs.md`

## 计算范围与限制

当前优化目标是：

> 在给定狂气、体力、模块、时间、通行证进度和资源储备要求的情况下，最大化通过普通镜牢与困难镜牢获得的循环自选人格碎片箱。

计算器不会自动统一估价以下内容：

- 限时活动商店
- 经验票和纺锤收益
- 主线与活动关卡的首次奖励
- 未经用户确认的维护、故障或活动补偿
- 玩家实际完成镜牢所需时间
- 抽取限定人格或E.G.O的战略价值
- 娱乐体验和重复刷取疲劳

计算器目前按规划期汇总可用资源，不会逐小时模拟每一笔奖励的实际到账顺序。跨赛季规划也需要根据新赛季规则重新核对。

因此，“箱子数量最大化”不一定等于“账号整体价值最大化”。计算结果应作为资源规划参考，而不是唯一正确的游玩方式。

## 数据来源

主要参考：

- [Limbus Company FAQ](https://faq.limbuscompany.site/)
- [Enkephalin](https://limbuscompany.wiki.gg/wiki/Enkephalin)
- [Lunacy](https://limbuscompany.wiki.gg/wiki/Lunacy)
- [Mirror Dungeons](https://limbuscompany.wiki.gg/wiki/Mirror_Dungeons)
- [Mirror of Names and Spiders](https://limbuscompany.wiki.gg/wiki/Mirror_of_Names_and_Spiders)
- [Limbus Pass](https://limbuscompany.wiki.gg/wiki/Limbus_Pass)
- [Season 7](https://limbuscompany.wiki.gg/wiki/Season_7)
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
