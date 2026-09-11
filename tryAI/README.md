# tryAI

A ChatGPT-style chat interface built with plain HTML, CSS and JavaScript, powered by a DeepSeek model hosted on Modal.
Built by **Bharat**.

## Why there's a `server.js` at all

Your Modal token (`MODAL_PROXY_TOKEN_ID` / `MODAL_PROXY_TOKEN_SECRET`) is a secret. If it's placed in browser-side
JavaScript, anyone who opens dev tools, views page source, or checks the Network tab can copy it and use your
endpoint on your bill. `server.js` is a ~70-line Express proxy that keeps the token on the server and only ever
sends the model's reply down to the browser. The actual UI — everything the user sees and interacts with — is
still 100% plain HTML/CSS/JS in `public/`.

## Project structure

```
tryAI/
├── server.js           # Express proxy -> Modal endpoint (keeps secret safe, streams SSE)
├── package.json
├── .env.example         # copy to .env and fill in your real values
├── public/
│   ├── index.html        # ChatGPT-style layout
│   ├── style.css          # dark/light theme, matches ChatGPT's visual language
│   └── script.js           # chat state, streaming, markdown-lite rendering
└── README.md
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure your secrets:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env`:
   ```
   MODAL_PROXY_TOKEN_ID=your_actual_token_id
   MODAL_PROXY_TOKEN_SECRET=your_actual_token_secret
   MODAL_BASE_URL=https://bhartshukla0501200--ep-deepseek-v4-1-flash-server.us-west.modal.direct/v1
   MODEL_NAME=deepseek-ai/DeepSeek-V4.1-Flash
   ```

3. Run it:
   ```bash
   npm start
   ```
   Open **http://localhost:3000**

## Features

- ChatGPT-style layout: collapsible sidebar, chat history, centered composer, suggestion chips on empty state
- Real streaming responses (token-by-token) via Server-Sent Events
- Multiple conversations, stored in the browser (`localStorage`) — new chat, switch chat, delete chat
- Dark / light theme toggle (persisted)
- Fenced code block + inline code rendering, auto-resizing input, Enter to send / Shift+Enter for newline
- Fully responsive down to mobile

## Notes for your submission

- `.env` is never sent to the browser — only `server.js` reads it (via `dotenv`), so your credentials stay private
  even if you deploy this or share the repo. Make sure `.env` is in `.gitignore` before pushing to GitHub.
- To change the model's personality, edit the `system` message in `server.js`.
- To deploy (e.g. Render, Railway, a college server), just set the same three env vars there and run `npm start`.
