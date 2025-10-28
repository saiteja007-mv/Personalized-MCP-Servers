# 🌤️ Weather MCP Server

A Model Context Protocol (MCP) server that provides **real-time and forecast weather data** using the **Open-Meteo API** — no API key required.

---

## 🧰 Features
- Get current weather by **city name**
- Get detailed weather by **coordinates**
- Get **5-day forecast**
- Uses **Open-Meteo.com** APIs

---

## 🐳 Run with Docker
```bash
docker build -t weather-mcp .
docker run -p 8000:8000 weather-mcp
