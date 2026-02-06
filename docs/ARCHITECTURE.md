# 🏗️ System Architecture

The **Autonomous Research Grid** is a sophisticated multi-agent system designed for deep informational synthesis. It leverages a dual-layer architecture consisting of a high-performance Spring Boot backend and a cinematic React frontend.

## 🤖 Multi-Agent Swarm

The core of the system is the **Intelligence Swarm**, which consists of four specialized agents working in a sequential pipeline:

1.  **🔎 Researcher Agent**:
    - **Role**: Information retrieval.
    - **Task**: Scours large-scale knowledge bases (or simulated datasets) for primary and secondary sources.
    - **Focus**: Breadth of knowledge and source reliability.

2.  **⚖️ Critic Agent**:
    - **Role**: Logical validation and bias detection.
    - **Task**: Challenges the findings of the Researcher, identifies logical gaps, and ensures neutrality.
    - **Focus**: Accuracy and objectivity.

3.  **🧬 Synthesizer Agent**:
    - **Role**: Data merging and pattern recognition.
    - **Task**: Combines the verified data from the Researcher and the feedback from the Critic into a structured outline.
    - **Focus**: Cohesion and insight generation.

4.  **📝 Writer Agent**:
    - **Role**: Final report production.
    - **Task**: Translates the synthesis into high-quality, professional Markdown documentation.
    - **Focus**: Clarity, tone, and formatting.

## ⚡ Fallback & Simulation Logic

To ensure 100% uptime during demonstrations, the system implements a **Bulletproof Fallback Pattern**:

- **Primary Path**: Frontend → Spring Boot API → OpenAI GPT-4.
- **Secondary Path (Autonomous Mode)**: If the backend is unreachable (e.g., local development or API limits), the frontend's internal **Antigravity Engine** takes over. It simulates the agent workflow and generates a context-aware mock report, ensuring the UI flow remains intact.

## 🛠️ Infrastructure

- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Framer Motion.
- **Backend**: Java 17, Spring Boot 3.2, Spring AI.
- **Deployment**: Vercel (Frontend), [Backend Service] (optional).
