# MindExecutor – API Action Proxy

🧠 Универсальный backend для ChatGPT Custom GPT, ассистентов и автоматизации действий через API.  
Поддерживает масштабируемые вызовы к сервисам:

- ✅ Trello (через key/token)
- ✅ Notion (через Bearer + Notion-Version)
- ✅ Google Drive (OAuth Bearer Token)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск локально

Создайте `.env` на основе `.env.example`:

```
TRELLO_KEY=your_trello_key
TRELLO_TOKEN=your_trello_token
NOTION_TOKEN=your_notion_token
GDRIVE_TOKEN=your_google_drive_token
```

Запустите сервер:

```bash
uvicorn app.main:app --reload
```

---

## 🧠 Как использовать

POST `/proxy`

```json
{
  "service": "trello",
  "method": "POST",
  "url": "/cards",
  "params": {
    "idList": "your_list_id",
    "name": "Задача",
    "desc": "Создано через GPT"
  }
}
```

---

## 📦 Поддержка сервисов

| Сервис        | Поле `service` |
|---------------|----------------|
| Trello        | `"trello"`     |
| Notion        | `"notion"`     |
| Google Drive  | `"gdrive"`     |

---

## 📡 Деплой на Railway

1. Залей в GitHub
2. Подключи к Railway
3. Добавь переменные в разделе Variables
4. Получи публичный API-адрес

---

## 📃 Лицензия

MIT — Используй, масштабируй, улучшай.