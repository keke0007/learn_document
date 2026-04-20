<h1>Anthropic《Harness design for long-running application development》阅读笔记</h1>
<ul>
<li>原文链接: <a href="https://www.anthropic.com/engineering/harness-design-long-running-apps" rel="nofollow">https://www.anthropic.com/engineering/harness-design-long-running-apps</a></li>
<li>作者: Prithvi Rajasekaran</li>
<li>发布时间: 2026-03-24</li>
<li>笔记目标: 提炼这篇文章关于 <code>long-running agent harness</code> 的核心思想、架构演进、成本收益权衡，以及可迁移到实际工程中的方法论。</li>
</ul>
<hr>
<h2>1. 一句话结论</h2>
<p>这篇文章最重要的判断是:</p>
<blockquote>
<p>当任务逼近模型的能力边界时，好的 <code>harness</code> 仍然能显著提升结果质量；但 harness 不是越复杂越好，而是要随着模型升级，持续剔除那些已经不再“承重”的组件。</p>
</blockquote>
<hr>
<h2>2. 先解释什么是 Harness</h2>
<p>在这篇文章里，<code>harness</code> 可以理解为:</p>
<ul>
<li>围绕模型执行任务的一层“运行框架”</li>
<li>它不只是 prompt，还包括:
<ul>
<li>角色分工</li>
<li>任务拆解</li>
<li>上下文传递</li>
<li>评估与验收机制</li>
<li>工具使用方式</li>
<li>多轮反馈循环</li>
</ul>
</li>
</ul>
<p>简单说:</p>
<ul>
<li><code>模型</code> 决定“能力上限”</li>
<li><code>harness</code> 决定“能力能否稳定落地”</li>
</ul>
<hr>
<h2>3. 作者要解决的两个根问题</h2>
<h3>3.1 长任务中的上下文退化</h3>
<p>同一个 agent 长时间工作后，容易出现:</p>
<ul>
<li>任务跑偏</li>
<li>局部遗忘</li>
<li>逻辑一致性下降</li>
<li>接近上下文极限时提前收尾</li>
</ul>
<p>文章里把后一种现象称为 <code>context anxiety</code>。</p>
<h3>3.2 Agent 的自评偏宽松</h3>
<p>当同一个 agent 既负责生成结果，又负责评估结果时，常见问题是:</p>
<ul>
<li>会高估自己的产出质量</li>
<li>会把明显缺陷合理化</li>
<li>对主观任务尤其容易“自我表扬”</li>
<li>在编码任务里也会漏掉边界 bug 和“看起来能跑但实际不可用”的问题</li>
</ul>
<hr>
<h2>4. 核心思路总览</h2>
<p>作者的整体思路可以概括为两句:</p>
<ol>
<li>把“生成”和“评估”拆开。</li>
<li>把“主观质量”改写成“可评分标准”。</li>
</ol>
<hr>
<h2>5. 架构演进图</h2>
<pre><code>flowchart LR
    A[&#34;朴素单代理\n收到一句需求后直接开工&#34;] --&gt; B[&#34;前端实验\nGenerator + Evaluator&#34;]
    B --&gt; C[&#34;全栈 V1\nPlanner + Generator + Evaluator\n按 Sprint 迭代&#34;]
    C --&gt; D[&#34;全栈 V2\n保留 Planner / Evaluator\n移除 Sprint&#34;]
    D --&gt; E[&#34;结论\n模型变强后，Harness 应持续瘦身\n但不会消失&#34;]
</code></pre>
<hr>
<h2>6. 前端设计实验: 把主观美感变成可评分问题</h2>
<p>作者先在前端设计上做实验，因为这里最容易暴露“自评不可信”的问题。</p>
<p>默认情况下，模型往往会生成:</p>
<ul>
<li>安全</li>
<li>稳妥</li>
<li>功能完整</li>
<li>但视觉上平庸、模板化、缺乏独特性的页面</li>
</ul>
<h3>6.1 四个评分维度</h3>
<p>| 维度 | 关注点 | 文章中的作用 |
| --- | --- | --- |
| Design quality | 整体视觉是否统一、是否形成完整气质 | 防止页面只是零散元素拼装 |
| Originality | 是否有真正的创意选择，而不是套模板 | 抑制“AI slop”与默认组件感 |
| Craft | 字体、间距、色彩、对比度等基本功 | 保证实现不粗糙、不失衡 |
| Functionality | 是否清楚、可用、容易完成任务 | 保证产品不只是“好看” |</p>
<h3>6.2 作者的关键强调</h3>
<p>作者明确强调:</p>
<ul>
<li><code>Design quality</code> 和 <code>Originality</code> 的权重大于 <code>Craft</code> 和 <code>Functionality</code></li>
</ul>
<p>原因是:</p>
<ul>
<li>模型在 craft 和 functionality 上本来就相对不差</li>
<li>真正拉不开差距的，是是否敢于摆脱“安全但平庸”的默认解</li>
</ul>
<h3>6.3 设计实验工作流</h3>
<pre><code>flowchart TD
    U[&#34;用户需求&#34;] --&gt; G[&#34;Generator 生成前端&#34;]
    G --&gt; E[&#34;Evaluator 使用 Playwright\n真实浏览与操作页面&#34;]
    E --&gt; S[&#34;按 4 个维度打分\n并给出详细批评&#34;]
    S --&gt; D{&#34;继续当前方向\n还是整体换风格?&#34;}
    D --&gt; G
</code></pre>
<h3>6.4 这一部分最值得记住的洞见</h3>
<h4>洞见 1: 主观问题也可以被工程化</h4>
<p>不是直接问:</p>
<ul>
<li>“这个设计美吗？”</li>
</ul>
<p>而是改成:</p>
<ul>
<li>“它是否符合我们定义的好设计原则？”</li>
</ul>
<p>后者更稳定、更可迭代。</p>
<h4>洞见 2: 评价标准不仅在评分，也在塑造输出</h4>
<p>作者提到，像 “museum quality” 这样的描述会反过来影响模型的设计方向。</p>
<p>这意味着:</p>
<ul>
<li>评分标准不是纯被动规则</li>
<li>它本身就是一种“美学 steering”</li>
</ul>
<h4>洞见 3: 迭代通常有提升，但不保证最后一轮一定最好</h4>
<p>文章提到:</p>
<ul>
<li>分数整体会提高</li>
<li>但人类偏好未必严格单调</li>
<li>中间轮次有时反而比最终轮次更讨喜</li>
</ul>
<p>这个结论说明，多轮优化是“提高命中率”，不是“保证最终最优”。</p>
<hr>
<h2>7. 长任务编码中的关键难点</h2>
<p>作者将前端实验的经验迁移到完整应用开发中，发现两个原始难点仍然成立:</p>
<ul>
<li>长上下文导致任务 coherence 下降</li>
<li>自评偏宽松导致质量门槛失守</li>
</ul>
<p>但在全栈编码里，还多了两个工程现实问题:</p>
<ul>
<li>需求太短时，模型容易欠规划</li>
<li>“看起来像完成”不等于“真的能用”</li>
</ul>
<hr>
<h2>8. Context Reset vs Compaction 对比</h2>
<p>| 维度 | Compaction | Context Reset |
| --- | --- | --- |
| 原理 | 压缩历史，继续沿同一会话工作 | 清空上下文，让新 agent 接力 |
| 优点 | 保持连续性，交接成本低 | 能真正解除 context anxiety |
| 缺点 | 旧状态和心理负担可能残留 | 依赖高质量 handoff artifact |
| 适用场景 | 模型长上下文能力较强时 | 模型容易在长任务中焦虑和跑偏时 |
| 文中作用 | 在更强模型上可基本胜任 | 在旧版 harness 中是关键机制 |</p>
<h3>8.1 作者的演进判断</h3>
<ul>
<li>在旧版长任务 harness 中，<code>context reset</code> 很重要</li>
<li>到更强的模型版本后，持续会话 + 自动 compaction 已经能承担更多工作</li>
<li>这正是 harness 需要不断瘦身的原因</li>
</ul>
<hr>
<h2>9. 全栈 V1: 三代理架构</h2>
<p>在完整应用开发里，作者采用了三角色结构:</p>
<p>| 角色 | 职责 | 存在原因 |
| --- | --- | --- |
| Planner | 把 1 到 4 句话扩写成完整产品 spec | 避免生成器欠规划、做得太少 |
| Generator | 按 spec 实现应用 | 承担主要构建工作 |
| Evaluator | 通过 Playwright、API、数据库检查来验收 | 识别深层功能缺陷和未完成项 |</p>
<h3>9.1 V1 的关键结构</h3>
<p>V1 不是“直接三代理一起跑”，而是还有两层重要机制:</p>
<h4>机制 A: Sprint 化开发</h4>
<ul>
<li>整体任务按 sprint 拆成一小段一小段</li>
<li>每一轮只做一个明确功能块</li>
<li>降低长时间连续构建带来的失控风险</li>
</ul>
<h4>机制 B: Sprint Contract</h4>
<p>每次 sprint 开始前，generator 和 evaluator 先协商:</p>
<ul>
<li>这轮做什么</li>
<li>什么才算 done</li>
<li>如何验证 done</li>
</ul>
<p>它起到的作用像是:</p>
<ul>
<li>开发前的微型规格说明</li>
<li>同时也是验收前置</li>
</ul>
<p>也就是先定义“完成标准”，再编码。</p>
<h3>9.2 V1 通信方式</h3>
<p>作者没有让 agent 们主要依赖长对话，而是通过文件进行交接:</p>
<ul>
<li>一个 agent 写文件</li>
<li>下一个 agent 读文件并回应</li>
</ul>
<p>这种设计的优点是:</p>
<ul>
<li>handoff 更稳定</li>
<li>状态更结构化</li>
<li>更适合多轮长任务</li>
</ul>
<hr>
<h2>10. Solo vs Full Harness 对比</h2>
<p>作者用一个任务做了直观比较:</p>
<blockquote>
<p>构建一个 2D retro game maker，包含关卡编辑器、精灵编辑器、实体行为和可试玩模式。</p>
</blockquote>
<h3>10.1 成本和时长</h3>
<p>| 方案 | 时长 | 成本 |
| --- | --- | --- |
| Solo 单代理 | 20 分钟 | 9 美元 |
| Full Harness | 6 小时 | 200 美元 |</p>
<h3>10.2 结果差异图</h3>
<pre><code>flowchart TB
    A[&#34;同一条一句话需求&#34;] --&gt; B[&#34;Solo 单代理&#34;]
    A --&gt; C[&#34;Full Harness&#34;]

    B --&gt; B1[&#34;界面初看还行&#34;]
    B1 --&gt; B2[&#34;空间利用差&#34;]
    B2 --&gt; B3[&#34;流程提示弱&#34;]
    B3 --&gt; B4[&#34;核心玩法损坏\n实体不可正常操控&#34;]

    C --&gt; C1[&#34;Planner 扩展成完整 spec&#34;]
    C1 --&gt; C2[&#34;更多功能与更完整范围&#34;]
    C2 --&gt; C3[&#34;整体视觉更统一&#34;]
    C3 --&gt; C4[&#34;真正能试玩\n核心链路可工作&#34;]
</code></pre>
<h3>10.3 本质差异</h3>
<p>| 维度 | Solo | Full Harness |
| --- | --- | --- |
| 规格展开能力 | 弱 | 强 |
| 功能覆盖范围 | 偏少 | 更完整 |
| UI/交互 polish | 基础可看 | 明显更成熟 |
| 深层功能可靠性 | 容易“看起来行，实际坏” | 更接近真实可用 |
| QA 发现问题能力 | 基本靠生成器自觉 | 有独立 evaluator 持续找错 |</p>
<h3>10.4 文章里很有代表性的 QA 发现</h3>
<p>Evaluator 抓到的问题包括:</p>
<ul>
<li>矩形填充工具没有真正填满区域，只在起点和终点放置</li>
<li>删除实体的条件判断错误，导致 UI 可选中但不可删除</li>
<li>FastAPI 路由声明顺序问题，导致 <code>reorder</code> 被当成 <code>frame_id</code></li>
</ul>
<p>这说明 evaluator 的价值在于:</p>
<ul>
<li>它不只是再“看一眼”</li>
<li>而是在替代部分真实 QA 与 code review</li>
</ul>
<hr>
<h2>11. V1 为什么还需要继续简化</h2>
<p>作者并没有因为 V1 成功就停下，而是继续质疑:</p>
<ul>
<li>哪些组件是真的必需的</li>
<li>哪些只是模型还不够强时的临时支架</li>
<li>当模型升级后，原本必要的结构是否还继续值得保留</li>
</ul>
<p>这部分背后的方法论非常重要:</p>
<blockquote>
<p>每个 harness 组件，本质上都编码了一条“模型单靠自己还做不到什么”的假设。模型能力变了，这些假设就应该重新验证。</p>
</blockquote>
<hr>
<h2>12. 全栈 V2: 去掉 Sprint 的简化版 Harness</h2>
<p>随着模型升级到更强版本，作者尝试删除 <code>sprint</code> 这一层结构。</p>
<h3>12.1 V2 保留了什么</h3>
<ul>
<li>Planner</li>
<li>Generator</li>
<li>Evaluator</li>
</ul>
<h3>12.2 V2 删除了什么</h3>
<ul>
<li>每个 sprint 的显式拆分</li>
<li>每个 sprint 单独验收的流程</li>
</ul>
<h3>12.3 V2 的新运行方式</h3>
<ul>
<li>Planner 先产出完整 spec</li>
<li>Generator 连续长时间构建</li>
<li>Evaluator 在一轮 build 结束后做 QA</li>
<li>若 QA 未通过，则继续下一轮 build 修复</li>
</ul>
<hr>
<h2>13. V1 vs V2 对比</h2>
<p>| 维度 | V1 | V2 |
| --- | --- | --- |
| 模型背景 | 更早期能力边界 | 更强模型能力背景 |
| 任务拆解方式 | 显式 sprint | 不再显式 sprint |
| QA 介入节奏 | 每个 sprint 都介入 | 每轮 build 后介入 |
| 编排复杂度 | 高 | 较低 |
| 对模型的依赖 | 较少依赖模型自我规划 | 更依赖模型自身连续工作能力 |
| 作者判断 | 适合模型尚需强辅助时 | 适合模型能力提升后的简化形态 |</p>
<h3>13.1 作者的关键结论</h3>
<p><code>Evaluator</code> 不是永远必须，也不是永远可以删掉。</p>
<p>它是否值得保留，取决于:</p>
<ul>
<li>当前任务是否已经落到模型可以稳定 solo 完成的范围内</li>
</ul>
<p>也就是说:</p>
<ul>
<li>对模型能稳做的任务，evaluator 可能只是额外开销</li>
<li>对仍在模型能力边界上的任务，evaluator 依然非常值钱</li>
</ul>
<hr>
<h2>14. DAW 实验: V2 的结果</h2>
<p>作者用 V2 harness 测试了一个更复杂任务:</p>
<blockquote>
<p>在浏览器中基于 Web Audio API 构建一个全功能 DAW。</p>
</blockquote>
<h3>14.1 成本与时长分解</h3>
<p>| 阶段 | 时长 | 成本 |
| --- | --- | --- |
| Planner | 4.7 分钟 | 0.46 美元 |
| Build Round 1 | 2 小时 7 分钟 | 71.08 美元 |
| QA Round 1 | 8.8 分钟 | 3.24 美元 |
| Build Round 2 | 1 小时 2 分钟 | 36.89 美元 |
| QA Round 2 | 6.8 分钟 | 3.09 美元 |
| Build Round 3 | 10.9 分钟 | 5.88 美元 |
| QA Round 3 | 9.6 分钟 | 4.06 美元 |
| 总计 | 3 小时 50 分钟 | 124.70 美元 |</p>
<h3>14.2 成本占比图</h3>
<pre><code>pie showData
    title V2 Harness 成本结构
    &#34;Planner&#34; : 0.46
    &#34;Build&#34; : 113.85
    &#34;QA&#34; : 10.39
</code></pre>
<h3>14.3 最关键的观察</h3>
<p>从这个拆分能直接看出:</p>
<ul>
<li>成本的大头几乎都在 <code>Build</code></li>
<li><code>Planner</code> 成本极小</li>
<li><code>QA</code> 不是免费，但相对 build 仍然便宜</li>
</ul>
<p>因此如果目标是“降本但保性能”，优先应该研究:</p>
<ul>
<li>如何缩短 build 轮次</li>
<li>如何减少 generator 的返工</li>
</ul>
<p>而不是先把 planner 或 evaluator 砍掉。</p>
<hr>
<h2>15. QA 在 V2 里仍然抓到了什么</h2>
<p>即使模型更强，QA 仍然发现了真实缺口，比如:</p>
<ul>
<li>一些核心 DAW 功能只是“展示态”，没有足够交互深度</li>
<li>音频录制仍是 stub</li>
<li>音频片段 resize 与 split 未真正实现</li>
<li>效果器只有数值滑杆，没有可视化编辑能力</li>
</ul>
<p>这说明:</p>
<ul>
<li>更强模型会减少 scaffolding 需求</li>
<li>但不会自动消除“最后一公里”质量问题</li>
</ul>
<hr>
<h2>16. 文章最重要的 10 条方法论提炼</h2>
<h3>16.1 Harness 的价值集中在模型能力边界</h3>
<p>简单任务可能不值得复杂编排。</p>
<p>复杂任务尤其是:</p>
<ul>
<li>多模块</li>
<li>多轮验证</li>
<li>有 UI、后端、数据库联动</li>
<li>有真实可用性要求</li>
</ul>
<p>这类任务更可能从 harness 获得明显收益。</p>
<h3>16.2 生成与评估应尽量分离</h3>
<p>同一个 agent 做“产出 + 评审”，很容易宽松。</p>
<p>独立 evaluator 的价值不是神奇地更聪明，而是:</p>
<ul>
<li>更容易被调成“怀疑型”</li>
<li>更适合作为负反馈来源</li>
</ul>
<h3>16.3 主观质量要先被翻译成标准</h3>
<p>不管是设计还是产品质量，都应该避免空泛表述。</p>
<p>比如把:</p>
<ul>
<li>“做得好一点”</li>
</ul>
<p>转成:</p>
<ul>
<li>是否有完整视觉身份</li>
<li>是否明显摆脱模板默认值</li>
<li>是否具备清晰的功能主路径</li>
<li>是否能通过具体交互检查</li>
</ul>
<h3>16.4 先定义 done，再写代码</h3>
<p>Sprint contract 的本质很值得借鉴:</p>
<ul>
<li>开工前就约定成功标准与验证路径</li>
</ul>
<p>这能显著减少“做了很多，但不是要的那个东西”。</p>
<h3>16.5 文件化交接比纯对话更适合长任务</h3>
<p>文件交接的优点是:</p>
<ul>
<li>状态清晰</li>
<li>便于审计</li>
<li>更适合跨 session</li>
<li>更便于 agent 接力</li>
</ul>
<h3>16.6 不要默认 harness 越复杂越强</h3>
<p>复杂 harness 经常有:</p>
<ul>
<li>更高 token 成本</li>
<li>更长 wall-clock time</li>
<li>更复杂调试路径</li>
</ul>
<p>因此应始终追问:</p>
<ul>
<li>当前这个组件是否还在提供真实收益</li>
</ul>
<h3>16.7 模型升级后，应该重新做“承重件审查”</h3>
<p>可以把 harness 看成脚手架。</p>
<p>模型更强后:</p>
<ul>
<li>有些脚手架可以拆掉</li>
<li>但也可能解锁新的、更高层能力组合</li>
</ul>
<h3>16.8 Evaluator 的必要性是动态的</h3>
<p>不是固定 yes/no，而是一个边界问题:</p>
<ul>
<li>如果任务已落入模型稳定能力范围，evaluator 可省</li>
<li>如果任务仍在边界上，evaluator 仍值得</li>
</ul>
<h3>16.9 QA 不能只看代码，应真实操作产品</h3>
<p>文章中 evaluator 使用 Playwright 去:</p>
<ul>
<li>点 UI</li>
<li>测 API</li>
<li>查数据库状态</li>
</ul>
<p>这比只读 diff 更接近真实验收。</p>
<h3>16.10 真正可用的 agent 系统不是“自动写代码”，而是“自动闭环”</h3>
<p>文章最强的部分，不是模型写出了很多代码，而是:</p>
<ul>
<li>能规划</li>
<li>能执行</li>
<li>能被质疑</li>
<li>能返工</li>
<li>能再次验收</li>
</ul>
<p>这才是“长任务应用开发”的关键。</p>
<hr>
<h2>17. 一页版浓缩提炼</h2>
<p>如果只保留最精华的内容，我会把这篇文章压缩成下面这 8 条:</p>
<p>| 编号 | 高密度结论 |
| --- | --- |
| 1 | <code>Harness</code> 的价值在于让模型能力稳定落地，而不是提升模型理论上限。 |
| 2 | 长任务最容易死在两点: <code>上下文退化</code> 与 <code>自评失真</code>。 |
| 3 | 最有效的基本结构是把 <code>生成</code> 与 <code>评估</code> 拆开。 |
| 4 | 对主观问题，先设计评分标准，再谈优化循环。 |
| 5 | 对复杂应用，先由 <code>planner</code> 扩写 spec，再让 <code>generator</code> 执行，会显著减少欠规划。 |
| 6 | <code>Evaluator</code> 最有价值的地方不是“挑刺”，而是把系统逼向真实可用。 |
| 7 | 模型升级后，应该优先删除已经不再承重的结构，不要盲目保留旧 scaffolding。 |
| 8 | 多 agent 的关键不是数量，而是有没有形成规划、执行、验收、返工的闭环。 |</p>
<hr>
<h2>18. 如果把它迁移到自己的 Agent 系统，建议这样落地</h2>
<h3>18.1 最小可用版本</h3>
<p>如果你想把这篇文章的方法迁移到自己的系统，我建议从下面这个最小组合开始:</p>
<p>| 组件 | 是否建议优先保留 | 原因 |
| --- | --- | --- |
| Planner | 是 | 防止任务欠规划、范围偏小 |
| Generator | 是 | 主执行器，必选 |
| Evaluator | 是 | 作为独立质量门槛，尤其在复杂任务上 |
| Sprint | 视模型能力而定 | 模型弱时有用，模型强时可尝试删除 |
| Context reset | 视模型长任务能力而定 | 若存在明显 context anxiety，就保留 |</p>
<h3>18.2 一个实用判断公式</h3>
<p>可以用下面这个思路判断要不要上复杂 harness:</p>
<pre><code>如果任务 = 长时 + 多模块 + 有 UI/后端/数据联动 + 需要真实验收
那么:
  先上 planner + evaluator
  再视情况增加 sprint / reset
否则:
  尽量保持简单
</code></pre>
<h3>18.3 一条工程化原则</h3>
<p>不要问:</p>
<ul>
<li>“这个 harness 看起来高级吗？”</li>
</ul>
<p>而要问:</p>
<ul>
<li>“它是否真正解决了当前模型在这个任务上的失败模式？”</li>
</ul>
<hr>
<h2>19. 我对这篇文章的评价</h2>
<p>我认为这篇文章最有价值的地方，不是展示了一个更复杂的 agent 系统，而是给出了一套很清楚的工程判断框架:</p>
<ul>
<li>先识别失败模式</li>
<li>再为失败模式加结构</li>
<li>模型升级后，再移除不再需要的结构</li>
</ul>
<p>它不是鼓吹“永远多代理”，而是在讲:</p>
<ul>
<li><code>什么时候多代理真的有用</code></li>
<li><code>什么时候复杂度会反噬</code></li>
<li><code>什么时候该做减法</code></li>
</ul>
<p>这比单纯展示 demo 更有参考价值。</p>
<hr>
<h2>20. 适合复用的讨论框架</h2>
<p>如果后续你要评估任何一个 agent 系统，可以直接用下面这套问题去看:</p>
<ol>
<li>这个系统的主要失败模式是什么:
<ul>
<li>欠规划</li>
<li>长上下文跑偏</li>
<li>自评偏宽松</li>
<li>验收不充分</li>
</ul>
</li>
<li>每个 harness 组件分别在修哪个失败模式</li>
<li>这些组件是否真的仍然承重</li>
<li>模型升级后，哪些组件可以删</li>
<li>对当前任务，收益最大的不是“再加 agent”，而是哪一个质量闭环环节</li>
</ol>
<hr>
<h2>21. 最终结论</h2>
<p>这篇文章真正想表达的是:</p>
<ul>
<li>长任务应用开发不是“让一个大模型持续写很久”</li>
<li>而是给模型搭一套能规划、执行、评审、返工、再验收的工作闭环</li>
</ul>
<p>随着模型变强:</p>
<ul>
<li>闭环不会消失</li>
<li>但闭环的结构会变化</li>
</ul>
<p>所以最值得学习的不是某个固定三代理模板，而是作者的工作方法:</p>
<blockquote>
<p>持续识别当前模型的真实短板，为这些短板加最小必要结构；当模型进步后，再主动把旧结构拆掉。</p>
</blockquote>
