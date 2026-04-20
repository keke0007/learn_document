<h1>AI Agent Harness 可复用设计模板</h1>
<ul>
<li>模板用途: 用于设计可长时间运行、可验收、可迭代返工的 AI agent harness</li>
<li>适用任务: 长任务编码、全栈应用搭建、复杂文档生产、研究代理、多步骤自动化执行</li>
<li>设计原则: <code>先找失败模式，再加结构；模型升级后，再删掉不再承重的结构</code></li>
</ul>
<hr>
<h2>1. 使用方式</h2>
<p>这不是一篇解释性文章，而是一份可直接套用的模板。</p>
<p>建议使用方法:</p>
<ol>
<li>先填写第 2 节的项目定义</li>
<li>再填写第 3 节的失败模式诊断</li>
<li>根据第 4 节选择 harness 档位</li>
<li>按第 5 到第 11 节完成角色、交接物、验收、循环设计</li>
<li>最后用第 12 节检查哪些结构是真正“承重”的</li>
</ol>
<hr>
<h2>2. 项目定义模板</h2>
<p>先不要急着设计 agent，先把任务边界写清楚。</p>
<h3>2.1 项目卡片</h3>
<pre><code>项目名称:
目标产物:
输入形式:
输出形式:
主要用户:
完成标准:
非目标范围:
最大允许时长:
最大允许成本:
必须使用的工具:
禁止事项:
</code></pre>
<h3>2.2 示例</h3>
<pre><code>项目名称: 浏览器端音乐工作站生成器
目标产物: 一个可运行的 Web DAW 应用
输入形式: 用户一句话需求
输出形式: 前端 + 后端 + 数据库 + 可运行 demo
主要用户: 想快速生成创作工具的独立开发者
完成标准: 可创建轨道、编辑片段、回放音频、保存工程，并通过 QA 的关键交互检查
非目标范围: 不追求专业级音频算法，不接入商业支付
最大允许时长: 4 小时
最大允许成本: 150 美元
必须使用的工具: git, 浏览器自动化, 构建命令, 测试命令
禁止事项: 不允许只做静态界面占位，不允许核心功能 stub 化后宣称完成
</code></pre>
<hr>
<h2>3. 失败模式诊断模板</h2>
<p>Harness 不是越复杂越好。先写清楚当前任务里最可能失败的地方。</p>
<h3>3.1 失败模式表</h3>
<p>| 失败模式 | 具体表现 | 严重度 | 可能对策 |
| --- | --- | --- | --- |
| 欠规划 | 直接开工，功能范围明显偏小 | 高 | 增加 planner |
| 长上下文跑偏 | 中途忘记目标、越做越散 | 高 | 增加 sprint / context reset / 文件交接 |
| 自评偏宽松 | 明明没做完却给自己通过 | 高 | 增加 evaluator |
| 验收不充分 | 页面能打开，但关键链路是坏的 | 高 | 加 Playwright / API / DB 检查 |
| 过度规定实现 | 上游 spec 锁死错误技术细节 | 中 | planner 只写产品目标和高层设计 |
| 成本失控 | 多轮返工导致 token 和时长爆炸 | 中 | 限制回合数，记录阶段成本 |
| 工具使用浅尝辄止 | 只读代码，不真实操作产品 | 中 | 要求 evaluator 做真实交互验证 |
| handoff 丢信息 | 多 agent 接力后状态错乱 | 高 | 文件化交接，固定 artifact 模板 |</p>
<h3>3.2 诊断结论模板</h3>
<pre><code>本任务的前三大失败模式:
1.
2.
3.

因此本次 harness 最少需要的结构:
- 
- 
- 

本次明确不引入的结构:
- 
- 原因:
</code></pre>
<hr>
<h2>4. Harness 档位选择模板</h2>
<p>先决定你需要的是轻量、中量还是重型 harness。</p>
<h3>4.1 档位选择表</h3>
<p>| 档位 | 适用任务 | 推荐结构 | 成本 |
| --- | --- | --- | --- |
| L1 轻量 | 短任务、单模块、结果容易验证 | <code>单代理 + 基础工具 + 最终检查</code> | 低 |
| L2 中量 | 中等复杂度、多步骤、有 UI 或数据联动 | <code>Planner + Generator + 最终 Evaluator</code> | 中 |
| L3 重型 | 长任务、多模块、联动复杂、易跑偏 | <code>Planner + Generator + Evaluator + Sprint/Contract + 文件交接</code> | 高 |</p>
<h3>4.2 决策规则</h3>
<pre><code>如果任务 = 短时 + 单模块 + 可快速验证
=&gt; 选 L1

如果任务 = 多步骤 + 有产品完整性要求 + 需要独立验收
=&gt; 选 L2

如果任务 = 长时 + 多模块 + 有 UI/后端/数据库联动 + 模型容易跑偏
=&gt; 选 L3
</code></pre>
<hr>
<h2>5. 标准角色模板</h2>
<p>不是每次都需要所有角色，但以下是最常见的可复用角色。</p>
<h3>5.1 Planner 模板</h3>
<p><strong>职责</strong></p>
<ul>
<li>把简短需求扩写成产品 spec</li>
<li>明确目标用户、核心场景、功能范围、成功标准</li>
<li>只写高层技术方向，不提前锁死过细实现细节</li>
</ul>
<p><strong>输入</strong></p>
<ul>
<li>用户原始需求</li>
<li>环境约束</li>
<li>已知技术栈</li>
</ul>
<p><strong>输出</strong></p>
<ul>
<li><code>product_spec.md</code></li>
</ul>
<p><strong>禁止</strong></p>
<ul>
<li>不要把所有技术细节一次性写死</li>
<li>不要直接替 generator 做实现决策</li>
</ul>
<p><strong>Prompt 骨架</strong></p>
<pre><code>你是 Planner。

任务:
把用户的一句话或短需求扩写成可执行的产品规格说明。

要求:
- 强化产品目标、目标用户、核心场景
- 给出高层功能结构与验收方向
- 可以提出雄心，但不要把细粒度实现写死
- 明确哪些能力必须真实可用，不能只是占位

输出文件:
- product_spec.md
</code></pre>
<h3>5.2 Generator 模板</h3>
<p><strong>职责</strong></p>
<ul>
<li>按 spec 构建系统</li>
<li>分阶段落地功能</li>
<li>遇到 evaluator 反馈后修复并继续推进</li>
</ul>
<p><strong>输入</strong></p>
<ul>
<li><code>product_spec.md</code></li>
<li><code>sprint_contract.md</code> 或 <code>qa_feedback.md</code></li>
</ul>
<p><strong>输出</strong></p>
<ul>
<li>代码改动</li>
<li>构建产物</li>
<li><code>build_notes.md</code></li>
</ul>
<p><strong>禁止</strong></p>
<ul>
<li>不要把 stub 功能当作完成</li>
<li>不要跳过失败验证</li>
<li>不要只看代码，不运行关键链路</li>
</ul>
<p><strong>Prompt 骨架</strong></p>
<pre><code>你是 Generator。

任务:
根据规格说明构建可运行产物，并在每轮结束时记录:
- 已完成内容
- 未完成内容
- 已验证内容
- 风险点

行为要求:
- 优先构建真实可用的主路径
- 失败时先找根因再修补
- 接收到 QA 反馈后要逐项响应

输出:
- 代码
- build_notes.md
</code></pre>
<h3>5.3 Evaluator 模板</h3>
<p><strong>职责</strong></p>
<ul>
<li>独立评估 generator 的结果</li>
<li>真实操作产品而不是只读代码</li>
<li>给出明确通过/失败结论与修复建议</li>
</ul>
<p><strong>输入</strong></p>
<ul>
<li><code>product_spec.md</code></li>
<li><code>sprint_contract.md</code></li>
<li>当前运行环境</li>
</ul>
<p><strong>输出</strong></p>
<ul>
<li><code>qa_feedback.md</code></li>
<li><code>pass/fail</code></li>
</ul>
<p><strong>禁止</strong></p>
<ul>
<li>不要仅因“整体看起来不错”而放过核心缺陷</li>
<li>不要把边界问题和主路径问题混为一谈</li>
<li>不要只写模糊批评，必须写可执行发现</li>
</ul>
<p><strong>Prompt 骨架</strong></p>
<pre><code>你是 Evaluator。

任务:
独立验收当前产物，重点检查:
- 主路径是否真实可用
- 是否存在核心功能 stub
- UI / API / 数据状态是否一致
- 是否满足约定的完成标准

输出要求:
- 每个问题都要写清现象、影响、复现方式、优先级
- 明确给出 PASS 或 FAIL
- 不允许因为“已经做了很多”而降低标准
</code></pre>
<h3>5.4 可选角色</h3>
<p>| 角色 | 何时加入 | 职责 |
| --- | --- | --- |
| Researcher | 需求依赖外部知识、标准、竞品 | 收集事实与约束 |
| Reviewer | 代码库较大，需额外 code review | 从实现质量角度补充审查 |
| Recovery Agent | 长任务中断或崩溃风险高 | 接管 artifact 并恢复流程 |
| Cost Monitor | 成本严格受限 | 记录轮次、token、时长、停止条件 |</p>
<hr>
<h2>6. Artifact 设计模板</h2>
<p>长任务里最重要的不是“多聊”，而是“交接物稳定”。</p>
<h3>6.1 推荐文件结构</h3>
<pre><code>/harness
  /artifacts
    product_spec.md
    sprint_contract.md
    build_notes.md
    qa_feedback.md
    run_status.md
    final_report.md
</code></pre>
<h3>6.2 每个 artifact 的职责</h3>
<p>| 文件 | 维护者 | 作用 |
| --- | --- | --- |
| <code>product_spec.md</code> | Planner | 固定产品目标与范围 |
| <code>sprint_contract.md</code> | Generator + Evaluator | 定义本轮 done 与验证方式 |
| <code>build_notes.md</code> | Generator | 记录实现、验证、风险 |
| <code>qa_feedback.md</code> | Evaluator | 输出问题列表与通过结论 |
| <code>run_status.md</code> | Orchestrator | 记录当前轮次、状态、成本 |
| <code>final_report.md</code> | Orchestrator | 收口交付、总结风险 |</p>
<h3>6.3 <code>sprint_contract.md</code> 模板</h3>
<pre><code># Sprint Contract

轮次:
负责人:
范围:

本轮目标:
- 
- 
- 

必须通过的行为:
- 
- 
- 

验证方式:
- 构建:
- 测试:
- UI:
- API:
- 数据:

失败条件:
- 
- 

本轮通过标准:
- 
</code></pre>
<h3>6.4 <code>qa_feedback.md</code> 模板</h3>
<pre><code># QA Feedback

轮次:
结论: PASS / FAIL

总评:

发现列表:
1. 标题:
   - 严重度:
   - 现象:
   - 复现步骤:
   - 影响:
   - 建议修复:

2. 标题:
   - 严重度:
   - 现象:
   - 复现步骤:
   - 影响:
   - 建议修复:

必须修复项:
- 
- 

可延后项:
- 
- 
</code></pre>
<hr>
<h2>7. 评价标准模板</h2>
<p>Evaluator 最好不要“凭感觉”打分，而要有固定 rubric。</p>
<h3>7.1 通用评分表</h3>
<p>| 维度 | 关注点 | 阈值 | 是否一票否决 |
| --- | --- | --- | --- |
| Feature Completeness | 核心功能是否真实完成 | 8/10 | 是 |
| Functionality | 主路径是否可用 | 8/10 | 是 |
| Product Depth | 是否只是浅层展示 | 7/10 | 否 |
| UX / Visual Quality | 界面是否清楚、统一、可用 | 7/10 | 否 |
| Code Quality | 结构是否混乱、明显不可维护 | 6/10 | 否 |</p>
<h3>7.2 评分规则模板</h3>
<pre><code>评分原则:
- 主路径失败直接 FAIL
- 核心功能 stub 直接 FAIL
- 只做展示而无交互深度，不得视为完成
- 若 UI、API、数据库状态不一致，判为功能不完整
- 不因实现工作量大而降低验收标准
</code></pre>
<h3>7.3 设计类任务可选维度</h3>
<p>| 维度 | 含义 |
| --- | --- |
| Design Quality | 是否形成统一视觉身份 |
| Originality | 是否摆脱模板与默认组件感 |
| Craft | 间距、排版、色彩等基本功 |
| Functionality | 交互与信息架构是否可用 |</p>
<hr>
<h2>8. 运行循环模板</h2>
<p>这是最关键的一节。真正可用的 harness，不是“多角色”，而是“有闭环”。</p>
<h3>8.1 标准闭环</h3>
<pre><code>flowchart TD
    A[&#34;用户需求&#34;] --&gt; B[&#34;Planner 产出 product_spec&#34;]
    B --&gt; C[&#34;Generator 制定本轮计划或 contract&#34;]
    C --&gt; D[&#34;Generator 实现并做基础验证&#34;]
    D --&gt; E[&#34;Evaluator 独立验收&#34;]
    E --&gt; F{&#34;是否通过?&#34;}
    F -- &#34;否&#34; --&gt; G[&#34;输出 qa_feedback&#34;]
    G --&gt; C
    F -- &#34;是&#34; --&gt; H[&#34;汇总 final_report&#34;]
</code></pre>
<h3>8.2 Orchestrator 伪代码</h3>
<pre><code>1. 接收用户需求
2. planner 生成 product_spec
3. while 未达到完成标准:
   - generator 读取 spec 与上一轮反馈
   - generator 产出实现并执行基础验证
   - evaluator 独立验收
   - 若 fail:
       写 qa_feedback
       进入下一轮修复
   - 若 pass:
       break
4. 输出 final_report
</code></pre>
<h3>8.3 停止条件模板</h3>
<pre><code>停止条件:
- 所有一票否决项通过
- 主路径验证通过
- 没有未处理的高优先级缺陷
- 达到最大回合数
- 达到最大成本
- 发生外部阻塞
</code></pre>
<hr>
<h2>9. Context 管理模板</h2>
<p>不是每个任务都需要 context reset，但要有明确决策规则。</p>
<h3>9.1 决策表</h3>
<p>| 情况 | 建议 |
| --- | --- |
| 模型在长任务中仍能稳定连续工作 | 优先用 compaction |
| 模型开始提前收尾、混乱、重复 | 增加 context reset |
| 多 agent 频繁接力 | 强制文件化 handoff |
| 任务跨多小时或多天 | 保留 run_status 与阶段性总结 |</p>
<h3>9.2 handoff 模板</h3>
<pre><code># Handoff Summary

当前状态:
当前分支/版本:
已完成:
- 
- 

未完成:
- 
- 

当前阻塞:
- 

下一个 agent 的第一步:
- 

关键文件:
- 
- 

关键验证命令:
- 
- 
</code></pre>
<hr>
<h2>10. 验证策略模板</h2>
<p>验证要分层，不要只跑一个命令就宣布完成。</p>
<h3>10.1 验证分层</h3>
<p>| 层级 | 内容 | 示例 |
| --- | --- | --- |
| 文件层 | 语法、格式、结构 | lint, typecheck, schema 校验 |
| 单点层 | 与改动最相关的行为 | 单元测试、接口调用 |
| 集成层 | 跨模块关键链路 | 构建、联调、端到端 smoke |
| 交付层 | 用户真正关心的结果 | 手动路径检查、录屏、关键截图 |</p>
<h3>10.2 验证记录模板</h3>
<pre><code>验证记录:
- [ ] 类型检查通过
- [ ] 构建通过
- [ ] 核心测试通过
- [ ] UI 主路径通过
- [ ] API 主路径通过
- [ ] 数据写入/读取正确
- [ ] 无高优先级已知缺陷
</code></pre>
<hr>
<h2>11. 成本与时长模板</h2>
<p>高质量 harness 往往昂贵，所以要主动记录成本。</p>
<h3>11.1 轮次记录表</h3>
<p>| 轮次 | 阶段 | 时长 | 成本 | 主要产出 | 是否通过 |
| --- | --- | --- | --- | --- | --- |
| 1 | Planner |  |  |  |  |
| 2 | Build |  |  |  |  |
| 3 | QA |  |  |  |  |
| 4 | Build |  |  |  |  |
| 5 | QA |  |  |  |  |</p>
<h3>11.2 成本复盘模板</h3>
<pre><code>本次成本最高的阶段:
原因:

返工主要来自:
- 
- 

下次可优化点:
- 减少哪些无效轮次
- 哪些标准可前置
- 哪些组件可删
</code></pre>
<hr>
<h2>12. 承重件审查模板</h2>
<p>这是整份模板里最关键的复盘动作。</p>
<p>每轮模型升级或系统升级后，都应该问:</p>
<h3>12.1 审查表</h3>
<p>| 组件 | 解决的失败模式 | 现在还在提供收益吗 | 是否可删 |
| --- | --- | --- | --- |
| Planner | 欠规划 |  |  |
| Evaluator | 自评失真、验收不足 |  |  |
| Sprint | 长任务跑偏 |  |  |
| Context Reset | context anxiety |  |  |
| 文件交接 | handoff 丢信息 |  |  |</p>
<h3>12.2 复盘问题</h3>
<pre><code>1. 如果删掉这个组件，结果会明显变差吗？
2. 这个组件现在是在补模型短板，还是只是历史遗留复杂度？
3. 它带来的收益，是否高于它增加的时长、成本和调试难度？
4. 是否有更轻的替代方案？
</code></pre>
<hr>
<h2>13. 一份可直接复制的最小模板</h2>
<p>如果你只想快速开工，可以直接从这个版本开始。</p>
<pre><code># Harness Blueprint

## 目标
- 用户需求:
- 最终产物:
- 完成标准:
- 最大时长:
- 最大成本:

## 失败模式
- 欠规划:
- 长任务跑偏:
- 自评偏宽松:
- 验收不足:

## 角色
- Planner: 负责产出 product_spec.md
- Generator: 负责按 spec 实现并记录 build_notes.md
- Evaluator: 负责独立验收并输出 qa_feedback.md

## Artifact
- product_spec.md
- build_notes.md
- qa_feedback.md
- final_report.md

## Rubric
- Feature Completeness:
- Functionality:
- Product Depth:
- UX / Visual Quality:
- Code Quality:

## 运行循环
1. Planner 产出 spec
2. Generator 实现主路径
3. Generator 执行基础验证
4. Evaluator 独立验收
5. FAIL 则返工，PASS 则收口

## 停止条件
- 主路径通过
- 无高优先级缺陷
- 达到最大回合数或成本上限时停止
</code></pre>
<hr>
<h2>14. 三种推荐落地版本</h2>
<h3>14.1 版本 A: 轻量版</h3>
<p>适合:</p>
<ul>
<li>小工具</li>
<li>单页应用</li>
<li>单文件脚本</li>
</ul>
<p>结构:</p>
<ul>
<li><code>Planner</code></li>
<li><code>Generator</code></li>
<li>最终一次 <code>Evaluator</code></li>
</ul>
<h3>14.2 版本 B: 标准版</h3>
<p>适合:</p>
<ul>
<li>中等复杂度产品</li>
<li>有前后端联动</li>
<li>有明确可用性要求</li>
</ul>
<p>结构:</p>
<ul>
<li><code>Planner</code></li>
<li><code>Generator</code></li>
<li><code>Evaluator</code></li>
<li>文件化 artifact</li>
<li>2 到 3 轮 build / QA</li>
</ul>
<h3>14.3 版本 C: 重型版</h3>
<p>适合:</p>
<ul>
<li>多小时任务</li>
<li>多模块应用</li>
<li>容易 context drift</li>
</ul>
<p>结构:</p>
<ul>
<li><code>Planner</code></li>
<li><code>Generator</code></li>
<li><code>Evaluator</code></li>
<li><code>Sprint Contract</code></li>
<li><code>run_status</code></li>
<li><code>Context Reset / Handoff</code></li>
</ul>
<hr>
<h2>15. 使用这份模板时最容易犯的错</h2>
<p>| 常见错误 | 为什么有害 | 修正方式 |
| --- | --- | --- |
| 一开始就上最复杂 harness | 成本高，调试难 | 先用最小可用结构 |
| 让 generator 自己验收自己 | 容易宽松 | 独立 evaluator |
| 只写“感觉还不错”的反馈 | 无法执行修复 | 反馈必须具体可复现 |
| 只看代码不操作产品 | 会漏掉大量交互问题 | 强制 UI/API/DB 联合检查 |
| spec 写太细 | 错误会级联放大 | planner 只写高层目标 |
| 不记录成本 | 无法复盘优化 | 强制记录轮次和耗时 |</p>
<hr>
<h2>16. 最终原则</h2>
<p>把这份模板真正用好，只要记住下面 4 句话:</p>
<ol>
<li>先诊断失败模式，再决定加什么 agent。</li>
<li>先定义完成标准，再进入实现。</li>
<li>让评估独立于生成。</li>
<li>模型升级后，优先删掉不再承重的结构。</li>
</ol>
