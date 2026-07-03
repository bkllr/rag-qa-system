# RAG QA System 问答系统介绍

## 系统概述

RAG QA System 是一个基于检索增强生成（RAG）架构的 AI 技术文档智能问答系统。

## 核心功能

- **技术问答**: 回答关于 Python、FastAPI、LangChain、Chroma、RAG、Vue3、深度学习、数据库、DevOps 等 100+ 个技术主题的问题
- **流式对话**: 支持 SSE（Server-Sent Events）流式输出，逐 token 实时显示回答，类似 ChatGPT 的打字机效果
- **来源追溯**: 每个回答附带文档来源引用，显示文件名和相似度分数（绿>80%、黄>60%、红<60%）
- **防幻觉约束**: Prompt 强制要求"只基于参考资料回答，找不到就说找不到"，杜绝 AI 胡编乱造

## 技术架构

- **后端**: FastAPI + LangChain LCEL + Chroma 向量数据库
- **Embedding**: text2vec-base-chinese（768 维本地中文向量模型）
- **LLM**: DeepSeek API（deepseek-chat 模型）
- **前端**: Vue 3 + Vite（SSE 流式渲染 + Markdown 代码高亮）
- **持久化**: Chroma 本地向量存储，断点重启无需重建

## 适用场景

- 技术学习辅助：快速查找技术概念、框架用法、代码示例
- 面试准备：检索技术知识点，附带准确来源
- 文档检索：对本系统内置的 100+ 篇技术文档进行智能问答
- 项目演示：展示 RAG 架构的完整实现，作为 AI 方向的简历项目

## 文档覆盖范围

系统索引了 102 篇技术文档，涵盖以下主题：
- Python 基础、FastAPI、Flask
- LangChain、LCEL、RAG 原理
- Chroma、FAISS 等向量数据库
- text2vec 中文 Embedding 模型
- Vue 3、Vite 前端框架
- DeepSeek、OpenAI 等 LLM API
- 小米开源项目（MACE、Open-Falcon、Pegasus）
- 数据库（MySQL、Redis、MongoDB）
- DevOps（Docker、Kubernetes、CI/CD）
- AI/ML、安全、通用编程

## 使用方式

1. 在输入框中输入技术问题（支持中文/英文）
2. 按 Enter 发送
3. AI 逐步流式输出回答
4. 回答完毕后自动显示参考来源
5. 点击来源卡片可展开查看引用原文

## 运行环境

- Python 3.10+（实际支持 3.9+）
- Node.js 18+
- DeepSeek API Key
- 首次运行自动下载 text2vec 模型（~500MB）并索引 102 篇文档
