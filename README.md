<p align="center">
  <a href="https://www.bilibili.com/video/BV1F2r5BCEiZ" target="_blank">
    <img src="https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/ospo-felizai.png" alt="Watch Demo Video" />
  </a>
  <br />
  👆 Click the image above to watch the demo video
</p>
<h1 align="center">Enterprise Open Source Governance Brain based on MaxKB and Feliz AI Knowledge Graph</h3>

<p align="center">
  <a href="README_CN.md"><img src="https://img.shields.io/badge/简体中文_README-blue" alt="Simplified Chinese README"></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.html#license-text"><img src="https://img.shields.io/github/license/1Panel-dev/maxkb?color=%231890FF" alt="License: GPL v3"></a>
  <a href="https://github.com/1Panel-dev/maxkb/releases/latest"><img src="https://img.shields.io/github/v/release/1Panel-dev/maxkb" alt="Latest release"></a>
</p>
<p align="center"> [<a href="/README_CN.md">中文(简体)</a>] | [<a href="/README.md">English</a>] </p>
<hr/>

[MaxKB](https://github.com/1Panel-dev/MaxKB) = Max Knowledge Brain, is a powerful and easy-to-use enterprise-grade agent platform. It is dedicated to solving problems such as high technical barriers, high deployment costs, and long iteration cycles in enterprise AI adoption, helping enterprises gain a head start in the AI era. Adhering to the "out-of-the-box, growing with you" design philosophy, MaxKB supports rapid integration of mainstream large models, efficient construction of exclusive knowledge bases, and provides a progressive upgrade path from basic Q&A (RAG) and complex process automation (Workflow) to Agents, fully empowering scenarios like intelligent customer service and intelligent office assistants.

[Feliz AI](https://www.felizai.cn/) (Shanghai Feliz Enterprise Management Co., Ltd.) is a vendor focusing on frontier AI technology consulting and product technical services, with rich practical experience in the application of industry knowledge graphs, natural language processing (NLP), and large language models (LLMs). The team's self-developed Feliz AI Knowledge Graph Automated Construction and Q&A Application Platform supports the integration of internal and external multi-source heterogeneous data. Through a dynamic ontology Schema framework, it achieves automated construction and unified fusion of knowledge graphs, enabling effective management and deep utilization of enterprise knowledge. It enhances the complex reasoning capabilities of large language models while effectively mitigating defects like model hallucinations.

- **Automated Modeling based on Dynamic Ontology**: Adopts a dynamic ontology Schema framework to support automated modeling and updating of domain knowledge, adapting to changing domain knowledge requirements, significantly shortening modeling time, and reducing modeling costs and risks.
- **Large-scale Knowledge Disambiguation and Refinement**: Algorithms support ultra-large-scale (billion-level entity) knowledge disambiguation, automatically identifying and handling "polysemy" and "synonymy" in knowledge, ensuring accuracy and consistency, and improving knowledge utilization and value.
- **Dynamic Reasoning for Complex Problems**: Addressing "hallucinations" and "uncontrollable logic" in large language models during complex reasoning and professional knowledge scenarios, Feliz AI has created an Agentic Workflow integrating capabilities such as complex problem decomposition, intent recognition, entity linking, and graph evidence chain traversal.

## Key Highlights

### 🚀 Technical Implementation
This competition solution not only implements basic RAG Q&A but also innovatively integrates **Feliz AI KAG (KnowledgeGraph Augmented Generation)**. By supporting knowledge graph-enhanced hybrid queries, we address the pain points of traditional RAG in complex reasoning scenarios, delivering agent Q&A results that exceed expectations.

### 💡 User Experience
Based on the out-of-the-box visual interface provided by MaxKB, it supports zero-code rapid construction of knowledge graphs embedded into the original MaxKB interaction flow. From knowledge base management and workflow orchestration to the final Q&A interface, every aspect is meticulously designed to ensure efficient information delivery and aesthetics, making complex AI technology accessible.

### 🔧 Technical Innovation
- **Hybrid Retrieval Architecture**: Combines vector retrieval, keyword retrieval, and graph retrieval, optimizing results through multi-way merge algorithms to significantly improve recall and accuracy.
- **Knowledge Graph Enhancement**: By integrating Feliz AI KAG, structured knowledge is introduced to enhance LLM logical reasoning capabilities, solving corner cases encountered by agents when performing complex tasks.
- **Heterogeneous Data Fusion**: Supports the integration of multi-source heterogeneous data, including structured data (using OpenDigger structured data for this project) and unstructured data (using Gitlab Handbook data), achieving unified data fusion and utilization.

### 🌐 Application Scenarios

- **Enterprise Knowledge Management**: Helps enterprises integrate and manage internal and external knowledge resources, improving decision-making efficiency and quality.
- **Intelligent Customer Service**: Provides 24/7 intelligent customer service support to resolve customer issues and needs, enhancing customer satisfaction.
- **Intelligent Office Assistant**: Provides intelligent office assistants for enterprise employees, helping them complete daily tasks and improve work efficiency.


## Contact Us

- [MaxKB + FelizAI KAG System Entry]([https://maxkb.felizai.cn/](https://maxkb.felizai.cn/chat/f87dc5d69cc9bf8e))

If you have more questions, feel free to communicate with us via WeChat.

- Scan the QR code below to add the Feliz AI representative.
<image height="400px" width="300px" src="https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/wechat.JPG"/>

## KAG vs. RAG Performance Comparison

<table style="border-collapse: collapse; border: 1px solid black;">
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/complex_query.png" alt="Complex Reasoning Query"   /></td>
  </tr>
  <tr>
    <td style="padding: 5px;background-color:#fff;"><img src= "https://feliz-0428.oss-cn-shanghai.aliyuncs.com/feliz/construct_query.png" alt="Structured Data Query"   /></td>
  </tr>
</table>

## Technical Stack

- Frontend: [Vue.js](https://vuejs.org/)
- Backend: [Python / Django](https://www.djangoproject.com/)
- LangChain: [LangChain](https://www.langchain.com/)
- Vector Database: [PostgreSQL / pgvector](https://www.postgresql.org/)
- Graph Database: [Neo4j](https://neo4j.com/)


## License

Licensed under The GNU General Public License version 3 (GPLv3)  (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<https://www.gnu.org/licenses/gpl-3.0.html>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
