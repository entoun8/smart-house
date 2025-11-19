@echo off
echo.
echo ========================================
echo  Deploying to Netlify...
echo ========================================
echo.

REM Commit and push changes
git add .
git commit -m "Update: Deploying latest changes"
git push

echo.
echo ✅ Pushed to GitHub!
echo ⏳ Netlify will auto-deploy in ~2-3 minutes
echo.
echo Check status at: https://app.netlify.com/sites/YOUR_SITE_NAME/deploys
echo.
pause
