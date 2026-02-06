# Multi-Agent AI Research Bot

A powerful Java Spring Boot application that orchestrates a team of AI agents to research, critique, synthesize, and write comprehensive reports. The system features a modern, premium React frontend for seamless interaction.

## 🏗 System Architecture

The system employs a sequential multi-agent workflow:
1.  **Researcher Agent**: Gathers comprehensive information on the topic.
2.  **Critic Agent**: Reviews the research for bias, gaps, and logical errors.
3.  **Synthesizer Agent**: Refines the content based on critique.
4.  **Writer Agent**: Produces the final polished report in Markdown format.

## 🛠 Tech Stack

### Backend
-   **Java 17**
-   **Spring Boot 3.2.4**
-   **Spring AI (OpenAI)**
-   **Lombok**

### Frontend
-   **React + Vite + TypeScript**
-   **Tailwind CSS** (Styling)
-   **Framer Motion** (Animations)
-   **Lucide React** (Icons)

## 🚀 Getting Started

### Prerequisites
-   Java 17+
-   Node.js 18+
-   Maven
-   OpenAI API Key

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Export your OpenAI API Key:
```bash
export OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
```

Run the application:
```bash
./mvnw spring-boot:run
# OR
mvn spring-boot:run
```
The backend API will start at `http://localhost:8080`.

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies (if not already done):
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
The frontend will open at `http://localhost:5173`.

## 🖥 Usage

1.  Open the web interface.
2.  Enter a complex research topic (e.g., "Impact of Quantum Computing on Cryptography").
3.  Click "Start Research".
4.  Watch the agents collaborate (Agents 1-4).
5.  View the final beautifully formatted report.

## 📂 Project Structure

```
/multi-agent-ai-research-bot
├── backend/                 # Spring Boot Backend
│   ├── src/main/java/...    # Agents, Orchestrator, Controller
│   └── pom.xml
└── frontend/                # React Frontend
    ├── src/...              # Components, Styles
    └── package.json
```
