@echo off
REM === Automated Blog Generation Script ===
REM Change directory to the project root (update path if needed)
cd /d %~dp0

REM Activate virtual environment if you use one (uncomment if needed)
REM call venv\Scripts\activate.bat

REM Run the full automation for an advanced SEO-friendly blog
python scripts\automated_blog_system.py advanced

REM Add all changes (blog HTML, images, blog-data.json, etc.)
git add blog-list\*.html blog-img\*.png blog-data.json

REM Commit with a timestamped message
set dt=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
git commit -m "Automated blog post: %dt%"

REM (Optional) Push to remote
REM git push

pause 