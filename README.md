# LangGraph MCP Assistant

## 📌 Overview

This is a simple AI assistant built using **LangGraph** and the **Model Context Protocol (MCP)**. It allows a language model to reason and interact with external tools through a graph-based execution flow.

The assistant can:

* 🌤️ Fetch **real-time weather** for any city
* 📰 Retrieve the **latest news** about any topic

All tools are exposed via individual MCP servers, and the assistant is powered by **Groq's LLaMA 3 model**.

---

## 🔧 Features

* ✅ MCP-compatible tool servers (weather, news)
* ✅ Multi-tool orchestration via `MultiServerMCPClient`
* ✅ LangGraph-based agent using ReAct framework
* ✅ Interactive CLI chat with agent (via `rich`)
* ✅ Environment variable support via `.env`

---

## 📂 Project Structure

```
.
├── client.py               # Main LangGraph agent client
├── weatherserver.py        # Weather tool MCP server
├── newsserver.py           # News tool MCP server
├── .env                    # API keys config
└── requirements.txt        # Dependencies
```

---

## 🚀 Quickstart

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Set Up `.env`

Create a `.env` file with the following keys:

```env
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
```

### 3. Run the Assistant

```bash
python client.py
```

You’ll see prompts like:

```
> What's the weather in Mumbai?
> Show me the latest news about AI
```

---

## 🧠 How It Works

* Each tool server is launched as a subprocess via `stdio`
* `FastMCP` exposes tool functions (like `get_weather`, `get_news`)
* The agent uses **LangGraph + ReAct** to decide when and how to call tools
* Tools return data → agent composes final reply

---

## 🔍 Example Tools

### 🌤️ Weather Tool

`weatherserver.py`

* Calls OpenWeatherMap API
* Returns city temperature, description, humidity, and wind speed

### 📰 News Tool

`newsserver.py`

* Calls NewsAPI
* Returns top headlines for a given topic (with description + link)

---

## 🧪 Sample Interactions

```bash
mcp> What's the weather in Delhi?
🤖 Agent: Weather in Delhi, IN: 34°C, clear sky. Humidity: 45%, Wind: 3 m/s

mcp> Show me news about AI
🤖 Agent: Latest news about 'AI':
1. OpenAI launches new tool...
2. AI used to detect fraud...
```

---

## 📃 License

MIT License

---

## 🙌 Credits

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [MCP](https://github.com/openai/mcp)
* [OpenWeatherMap](https://openweathermap.org/api)
* [NewsAPI](https://newsapi.org)
* [Groq](https://console.groq.com)
