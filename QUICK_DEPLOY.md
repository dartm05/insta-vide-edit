# 🚀 Quick Deploy to Railway

Deploy your Instagram Video Editor in **5 minutes**!

## Prerequisites

- Railway account (free): https://railway.app
- Node.js installed (for Railway CLI)

## Step-by-Step

### 1. Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login to Railway

```bash
railway login
```

A browser window will open. Sign in with GitHub.

### 3. Deploy from This Directory

```bash
# Make sure you're in the VideoAgent directory
cd /Users/daniellaarteagamendoza/Documents/Projects/VideoAgent

# Initialize Railway project
railway init

# When prompted:
# - Enter project name: "instagram-video-editor"
# - Choose: "Create new project"

# Deploy!
railway up
```

### 4. Get Your Live URL

```bash
railway domain
```

Or open in browser:
```bash
railway open
```

## ✅ That's It!

Your app is now live at: `https://[your-app].up.railway.app`

---

## Configuration (Optional)

### Set Environment Variables

```bash
# For AI features (optional)
railway variables set ANTHROPIC_API_KEY=your_key_here

# View all variables
railway variables
```

### View Logs

```bash
railway logs
```

### Redeploy

```bash
railway up
```

---

## What Gets Deployed

✅ Python 3.9 backend
✅ FFmpeg (for video processing)
✅ FastAPI web server
✅ All dependencies
✅ Static files (HTML/CSS/JS)

---

## Cost

- **Free Tier**: $5 credit/month
- **Usage**: ~$0.01 per video processed
- Most users stay within free tier

---

## Troubleshooting

### "railway: command not found"

Install Node.js first:
```bash
brew install node
npm install -g @railway/cli
```

### Deployment fails

Check logs:
```bash
railway logs
```

Common issues:
- Missing dependencies → Check `web_requirements.txt`
- Port issues → Railway auto-configures port 8000

### Can't upload videos

Check file size limits:
- Railway default: 100MB per file
- Increase in Railway dashboard if needed

---

## Next Steps

1. **Test the app** - Upload a video and process it
2. **Share the URL** - Give it to your team/users
3. **Monitor usage** - Check Railway dashboard
4. **Scale if needed** - Upgrade plan in Railway

---

## Alternative: One-Click Deploy

Coming soon! Railway deploy button for instant deployment.

For now, follow the steps above - it takes less than 5 minutes!
