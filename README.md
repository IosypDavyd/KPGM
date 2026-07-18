# 🎵 KPGM KEYPOWERGRAILMYSTERY MUSIC VIDEO GENERATOR

**Універсальне приложение для генерації музики і відео**

## 🚀 Особливості

- ✨ **SUNO AI Integration** - Генерація музики за текстовим описом
- 🎬 **Video Generation** - Автоматична генерація відео для музики
- 🎨 **AI Visual Effects** - Синтез видео за допомогою Runway/Stability AI
- 🔄 **Audio-Video Sync** - Синхронізація аудіо та відео
- 🌐 **Web UI** - Інтуїтивний веб-інтерфейс
- 📡 **REST API** - Повнофункціональний API
- 🎯 **Batch Processing** - Масова обробка проектів
- 💾 **Project Management** - Збереження і управління проектами

## 📋 Вимоги

- Python 3.9+
- Node.js 16+
- SUNO API Key
- Runway ML API Key (для відео)
- FFmpeg

## 🔧 Встановлення

```bash
# Клонування репозиторію
git clone https://github.com/IosypDavyd/KPGM.git
cd KPGM
git checkout music-video-generator

# Встановлення залежностей
pip install -r requirements.txt
npm install

# Конфігурація
cp .env.example .env
# Додайте API ключі в .env
```

## 🎯 Використання

### Web UI
```bash
python app.py
# Перейдіть на http://localhost:5000
```

### CLI
```bash
python cli.py --text "описание музики" --style "жанр" --duration 60
```

### API
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "описание музики",
    "style": "ambient",
    "duration": 60,
    "video": true
  }'
```

## 📁 Структура проекту

```
KPGM/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── api/
│   ├── services/
│   │   ├── suno_service.py
│   │   ├── video_service.py
│   │   └── synthesis_service.py
│   ├── models/
│   └── utils/
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── assets/
│   └── public/
├── ffmpeg_scripts/
├── docs/
└── tests/
```

## 🔐 Безпека

- Всі API ключі зберігаються в `.env`
- Аутентифікація через JWT
- CORS конфігурація
- Rate limiting

## 📚 Документація

Детальна документація знаходиться в папці `docs/`

## 🤝 Контрибьютинг

Вітаємо PR та Issues!

## 📄 Ліцензія

MIT License

## 🌟 Автор

**IosypDavyd** - KPGM Community
