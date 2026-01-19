<p align="center">
  <a href="https://www.bilibili.com/video/BV1F2r5BCEiZ" target="_blank">
    <img src="https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/ospo-felizai.png" alt="点击查看演示视频" />
  </a>
  <br />
  👆 点击图片查看演示视频
</p>
<h1 align="center">基于MaxKB与Feliz AI知识图谱的企业开源治理大脑</h3>

<p align="center">
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English_README-blue" alt="English README"></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.html#license-text"><img src="https://img.shields.io/github/license/1Panel-dev/maxkb?color=%231890FF" alt="License: GPL v3"></a>
  <a href="https://github.com/1Panel-dev/maxkb/releases/latest"><img src="https://img.shields.io/github/v/release/1Panel-dev/maxkb" alt="Latest release"></a>
</p>
<hr/>

[MaxKB](https://github.com/1Panel-dev/MaxKB) = Max Knowledge Brain，是一个强大易用的企业级智能体平台，致力于解决企业 AI 落地面临的技术门槛高、部署成本高、迭代周期长等问题，助力企业在人工智能时代赢得先机。秉承“开箱即用，伴随成长”的设计理念，MaxKB 支持企业快速接入主流大模型，高效构建专属知识库，并提供从基础问答（RAG）、复杂流程自动化（工作流）到智能体（Agent）的渐进式升级路径，全面赋能智能客服、智能办公助手等多种应用场景。

[Feliz AI](https://www.felizai.cn/) 上海赋立咨企业管理有限公司（Feliz AI）是一家专注于世界前沿AI技术咨询及产品技术服务的厂商，在行业知识图谱、自然语言处理和大语言模型等AI前沿技术的落地应用上拥有丰富的实践经验。团队自主研发的Feliz AI 知识图谱自动构建及问答应用平台，支持整合企业内外部多源异构的数据，通过动态本体论的 Schema 框架，实现知识图谱的自动构建与统一融合，实现了对企业知识的有效管理与深度利用。提升大语言模型复杂推理能力的同时有效弥补模型幻觉等缺陷。

- **基于动态本体论自动化建模**：采用动态本体论的 Schema 框架，支持领域内知识的自动化建模与更新，适应领域知识变化的需求，极大缩短知识建模的时间，降低了知识建模的成本和风险。
- **大规模知识自动消歧及精炼**：算法支持超大规模（十亿级别实体）的知识消歧，自动识别和处理知识中的“一词多义”和“多词一义”，确保知识的准确性和一致性，提高知识的利用率和价值。
- **针对复杂问题的动态推理**：解决大语言模型在复杂推理和专业知识场景下的“幻觉”与“逻辑不可控”问题，Feliz AI打造了的复杂问题拆解、意图识别、实体链接、图上证据链遍历等多种能力集成的Agentic Workflow。

## 核心亮点

### 🚀 技术实现 
本次比赛方案不仅实现了基础的 RAG 问答，更创新性地融合了 **Feliz AI KAG (KnowledgeGraph Augmented Generation)** 。通过支持知识图谱增强的混合查询，我们解决了传统RAG在复杂推理场景下的痛点，提供了超越预期的智能体问答效果。

### 💡 交互体验 
基于 MaxKB 提供开箱即用的可视化界面，支持零编码快速构建知识图谱，并嵌入 MaxKB 原先交互流程。无论是知识库管理、工作流编排还是最终的问答界面，都经过精心设计，确保信息传达的高效与美观，让复杂的 AI 技术变得触手可及。

### 🔧 技术创新 
- **混合检索架构**：结合向量检索、关键词检索和图谱检索，通过多路归并算法优化结果，显著提升召回率与准确性。
- **知识图谱增强**：通过集成Feliz AI KAG，引入结构化知识增强大模型逻辑推理能力，解决了 Agent 在执行复杂任务时遇到的长尾错误（Corner Cases）。
- **异构数据融合**：支持整合多源异构数据，包括结构化数据（本次采用 OpenDigger 的结构化数据）、非结构化数据（本次采用 Gitlab Handbook 手册数据），实现数据的统一融合和利用。

### 🌐 应用场景 

- **企业知识管理**：帮助企业整合和管理内部和外部的知识资源，提升决策效率和质量。
- **智能客服**：为客户提供24/7的智能客服支持，解决客户问题和需求，提升客户满意度。
- **智能办公助手**：为企业员工提供智能办公助手，帮助员工完成日常任务，提升工作效率。


## 联系我们

- [MaxKB + FelizAI KAG系统入口](https://maxkb.felizai.cn/chat/f87dc5d69cc9bf8e)

如你有更多问题，可以通过微信与我们交流。

- 扫描下方微信添加 Feliz AI 负责人
<image height="400px" width="300px" src="https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/wechat.JPG"/>

## KAG 与 RAG 效果对比展示

<table style="border-collapse: collapse; border: 1px solid black;">
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/complex_query.png" alt="Complex Reasoning Query"   /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/construct_query.png" alt="Structured Data Query"   /></td>
  </tr>
</table>

## 技术栈

- 前端：[Vue.js](https://cn.vuejs.org/)
- 后端：[Python / Django](https://www.djangoproject.com/)
- LangChain：[LangChain](https://www.langchain.com/)
- 向量数据库：[PostgreSQL / pgvector](https://www.postgresql.org/)
- 图数据库：[Neo4j](https://neo4j.com/)


## License

Licensed under The GNU General Public License version 3 (GPLv3)  (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<https://www.gnu.org/licenses/gpl-3.0.html>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
