@echo off
echo ========================================
echo    AUTOMATED BLOG SYSTEM
echo ========================================
echo.
echo 🤖 Running automated blog generation...
echo.
echo 📅 Schedule:
echo    - Monday: Advanced blog with code examples
echo    - Wednesday: SEO-optimized blog  
echo    - Friday: Simple daily blog
echo.
echo 🎨 Features:
echo    - AI image generation (Hugging Face/Together AI)
echo    - Automatic blog type selection
echo    - SEO optimization
echo    - Schema markup
echo    - Dynamic blog listing
echo.
python scripts/automated_blog_system.py
echo.
echo ========================================
echo ✅ Automated blog system completed!
echo ========================================
echo.
echo 💡 To set up automatic posting:
echo    1. Add API keys to GitHub Secrets
echo    2. Push to GitHub repository
echo    3. GitHub Actions will run automatically
echo.
echo 🔑 Required API Keys:
echo    - HF_TOKEN (Hugging Face)
echo    - TOGETHER_API_KEY (Together AI)
echo    - REPLICATE_API_TOKEN (Replicate)
echo.
echo 📚 Documentation: README.md
echo ========================================
pause 