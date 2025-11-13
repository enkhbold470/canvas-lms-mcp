# Dedalus Canvas

Day 7 of 30 days of coding

Canvas LMS integration with Dedalus Labs AI for course analysis and dashboard.

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`:
```env
CANVAS_API_KEY=your_key
CANVAS_BASE_URL=https://your-instance.instructure.com
DEDALUS_API_KEY=your_key
```

## Usage

**AI Analysis:**
```bash
python main.py
```

**Web Dashboard:**
```bash
python app.py
# http://localhost:5001
```

**Test API:**
```bash
python tool.py
```

## Files

- `tool.py` - Canvas API functions (courses, assignments, grades)
- `main.py` - AI analysis using DedalusRunner
- `app.py` - Flask dashboard with AI chat

## Dependencies

- dedalus-labs
- flask
- httpx
- python-dotenv
