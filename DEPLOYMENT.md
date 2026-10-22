# Deployment Guide

## Quick Deploy to Railway (Recommended)

Railway is the easiest way to deploy this application. It supports Python, FFmpeg, and file uploads out of the box.

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

### Step 3: Initialize and Deploy

```bash
# From the VideoAgent directory
railway init

# Deploy the application
railway up
```

### Step 4: Set Environment Variables (Optional)

If you want AI features (Phase 3), set your API key:

```bash
railway variables set ANTHROPIC_API_KEY=your_key_here
```

### Step 5: Open Your App

```bash
railway open
```

Your app will be live at a URL like: `https://your-app.up.railway.app`

---

## Alternative: Deploy to Render

### Step 1: Create a Render Account

Go to https://render.com and sign up.

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository (or upload code)
3. Configure:
   - **Name**: instagram-video-editor
   - **Environment**: Python 3
   - **Build Command**: `pip install -r web_requirements.txt`
   - **Start Command**: `python3 run_web.py`

### Step 3: Add FFmpeg Buildpack

In the "Environment" section, add:
```
PYTHON_VERSION=3.9
```

Render includes FFmpeg by default!

### Step 4: Deploy

Click "Create Web Service" and wait for deployment.

---

## Alternative: Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
brew install heroku/brew/heroku
```

### Step 2: Login and Create App

```bash
heroku login
heroku create your-app-name
```

### Step 3: Add FFmpeg Buildpack

```bash
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add --index 2 heroku/python
```

### Step 4: Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## Environment Variables

Set these environment variables in your deployment platform:

```bash
# Optional: For AI features (Phase 3)
ANTHROPIC_API_KEY=your_key_here

# Optional: Custom configuration
OUTPUT_DIR=/tmp/output
TEMP_DIR=/tmp/uploads
CACHE_DIR=/tmp/cache
```

---

## Post-Deployment Checklist

✅ App is accessible via URL
✅ Homepage loads correctly
✅ Can upload test video
✅ Video processing works
✅ Can download processed video

---

## Troubleshooting

### App doesn't start
- Check logs: `railway logs` or view in dashboard
- Verify all dependencies in `web_requirements.txt`
- Ensure Python 3.9+ is specified

### Video processing fails
- Verify FFmpeg is installed (check logs)
- Check file size limits (Railway: 100MB default)
- Ensure temp directories are writable

### Upload fails
- Check file size limits
- Verify `web/uploads/` directory exists
- Check disk space on deployment platform

---

## Cost Estimate

### Railway (Recommended)
- **Free Tier**: $5 credit/month
- **Hobby Plan**: $5/month (usually enough)
- Estimate: ~$0.01 per video processed

### Render
- **Free Tier**: Available (with limits)
- **Starter Plan**: $7/month
- Includes 100GB bandwidth

### Heroku
- **Free Tier**: Removed (as of 2022)
- **Hobby Plan**: $7/month
- Add-ons may be required

---

## Scaling Considerations

For high traffic:

1. **Use Redis** for job queue (instead of in-memory)
2. **Add Celery** for distributed processing
3. **Use S3** for file storage (instead of local disk)
4. **Enable caching** for style analysis results
5. **Set up CDN** for static assets

See `WEB_APP_GUIDE.md` for production deployment details.
