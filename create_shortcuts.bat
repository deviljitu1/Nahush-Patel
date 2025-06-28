@echo off
echo ========================================
echo    CREATING BLOG TOOL SHORTCUTS
echo ========================================
echo.

:: Get the current directory
set "CURRENT_DIR=%~dp0"

:: Create desktop shortcut for SEO blog generator
echo Creating shortcut for SEO Blog Generator...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Generate SEO Blog.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%generate_seo_blog.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Generate SEO-optimized blog posts with schema markup and slug-based URLs'; $Shortcut.Save()"

:: Create desktop shortcut for advanced blog generator
echo Creating shortcut for Advanced Blog Generator...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Generate Advanced Blog.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%generate_advanced_blog.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Generate advanced SEO-friendly blog posts with code examples'; $Shortcut.Save()"

:: Create desktop shortcut for daily blog generator
echo Creating shortcut for Daily Blog Generator...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Generate Daily Blog.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%generate_daily_blog.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Generate simple SEO-friendly blog posts'; $Shortcut.Save()"

:: Create desktop shortcut for update blogs
echo Creating shortcut for Update Blogs...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Update Blogs.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%update_blogs.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'Update blog listing and metadata'; $Shortcut.Save()"

echo.
echo ========================================
echo ✅ SHORTCUTS CREATED SUCCESSFULLY!
echo ========================================
echo.
echo 📁 Shortcuts created on your Desktop:
echo    - Generate SEO Blog.lnk (NEW!)
echo    - Generate Advanced Blog.lnk
echo    - Generate Daily Blog.lnk  
echo    - Update Blogs.lnk
echo.
echo 🎯 You can now:
echo    - Double-click any shortcut to run
echo    - Pin them to taskbar for quick access
echo    - Organize them in a folder
echo    - Customize icons and properties
echo.
echo 🚀 Happy Blogging!
echo ========================================
pause 