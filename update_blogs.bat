@echo off
echo ========================================
echo        BLOG UPDATE SYSTEM
echo ========================================
echo.
echo Updating blog data...
python scripts/blog_scanner.py
echo.
echo ========================================
echo Blog data updated successfully!
echo.
echo NEW BLOG FILES:
echo - Will automatically get current date/time
echo - Will appear at the top of the blog list
echo - No manual date entry needed!
echo.
echo To add a new blog:
echo 1. Copy blog-template.html to blog-list/
echo 2. Rename it to your-blog-name.html
echo 3. Edit the content
echo 4. Run this script again
echo ========================================
pause 