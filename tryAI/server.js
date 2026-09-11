// tryAI backend — Bharat
// Minimal proxy so the Modal token never touches the browser.
// Frontend (HTML/CSS/JS) talks to THIS server. THIS server talks to Modal.

require("dotenv").config();
const express = require("express");
const path = require("path");
const OpenAI = require("openai");

const app = express();
const PORT = process.env.PORT || 3000;

const MODAL_TOKEN_ID = process.env.MODAL_PROXY_TOKEN_ID;
const MODAL_TOKEN_SECRET = process.env.MODAL_PROXY_TOKEN_SECRET;
const MODAL_BASE_URL = process.env.MODAL_BASE_URL;
const MODEL_NAME = process.env.MODEL_NAME || "deepseek-ai/DeepSeek-V4.1-Flash";

if (!MODAL_TOKEN_ID || !MODAL_TOKEN_SECRET || !MODAL_BASE_URL) {
  console.error(
    "Missing env vars. Copy .env.example to .env and fill in MODAL_PROXY_TOKEN_ID, MODAL_PROXY_TOKEN_SECRET, MODAL_BASE_URL."
  );
  process.exit(1);
}

const client = new OpenAI({
  baseURL: MODAL_BASE_URL,
  apiKey: `${MODAL_TOKEN_ID}.${MODAL_TOKEN_SECRET}`,
});

app.use(express.json({ limit: "2mb" }));
app.use(express.static(path.join(__dirname, "public")));

// Simple health check
app.get("/api/health", (_req, res) => res.json({ ok: true }));

// Streaming chat endpoint (Server-Sent Events)
app.post("/api/chat", async (req, res) => {
  const { messages } = req.body;

  if (!Array.isArray(messages) || messages.length === 0) {
    return res.status(400).json({ error: "messages[] is required" });
  }

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();

  try {
    const stream = await client.chat.completions.create({
      model: MODEL_NAME,
      messages: [
        { role: "system", content: "You are tryAI, a helpful, concise technical assistant built by Bharat." },
        ...messages,
      ],
      temperature: 0.3,
      max_tokens: 2048,
      top_p: 0.9,
      stream: true,
    });

    for await (const part of stream) {
      const delta = part.choices?.[0]?.delta?.content;
      if (delta) {
        res.write(`data: ${JSON.stringify({ token: delta })}\n\n`);
      }
    }
    res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
    res.end();
  } catch (err) {
    console.error("Model error:", err);
    res.write(`data: ${JSON.stringify({ error: err.message || "Model request failed" })}\n\n`);
    res.end();
  }
});

app.listen(PORT, () => {
  console.log(`tryAI server running at http://localhost:${PORT}`);
});
