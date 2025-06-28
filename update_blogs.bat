@echo off
echo Updating blog data...
python scripts/blog_scanner.py
echo.
echo Blog data updated successfully!
echo New blog files will now appear at the top of the list.
pause 