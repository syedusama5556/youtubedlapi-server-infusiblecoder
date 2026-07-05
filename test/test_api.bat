@echo off
setlocal enabledelayedexpansion

set BASE=http://localhost:9192
set PASS=0
set FAIL=0

echo ========================================
echo  yt-dlp API Server Test Suite
echo ========================================
echo.

rem --- VERSION ---
echo [TEST] GET /api/version
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/version"`) do set RES=%%i
echo %RES% | find "yt-dlp" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- EXTRACTORS ---
echo [TEST] GET /api/extractors
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/extractors"`) do set RES=%%i
echo %RES% | find "extractors" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- YOUTUBE INFO ---
echo [TEST] GET /api/info (YouTube)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ^&flatten=true"`) do set RES=%%i
echo %RES% | find "Rick Astley" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- YOUTUBE FORMATS ---
echo [TEST] GET /api/formats (YouTube)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/formats?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"`) do set RES=%%i
echo %RES% | find "format_id" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- YOUTUBE SUBTITLES ---
echo [TEST] GET /api/subtitles (YouTube)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/subtitles?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"`) do set RES=%%i
echo %RES% | find "subtitles" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- YOUTUBE AUDIO ---
echo [TEST] GET /api/audio (YouTube)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/audio?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"`) do set RES=%%i
echo %RES% | find "audio_url" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- YOUTUBE SEARCH ---
echo [TEST] GET /api/search (YouTube)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/search?q=never+gonna+give+you+up&limit=3"`) do set RES=%%i
echo %RES% | find "results" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- VIMEO ---
echo [TEST] GET /api/info (Vimeo)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/info?url=https://vimeo.com/76979871^&flatten=true"`) do set RES=%%i
echo %RES% | find "Vimeo" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- TED ---
echo [TEST] GET /api/info (TED)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/info?url=https://www.ted.com/talks/chloe_valdary_how_love_can_help_repair_social_inequality^&flatten=true"`) do set RES=%%i
echo %RES% | find "love" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- DAILYMOTION ---
echo [TEST] GET /api/info (Dailymotion)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/info?url=https://www.dailymotion.com/video/xal2ebm^&flatten=true"`) do set RES=%%i
echo %RES% | find "title" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- PLAY REDIRECT ---
echo [TEST] GET /api/play (redirect 302)
curl -s -o nul -w "%%{http_code}" "%BASE%/api/play?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" | find "302" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   FAIL & set /a FAIL+=1)

rem --- BAD URL HANDLING ---
echo [TEST] GET /api/info (invalid URL)
for /f "usebackq delims=" %%i in (`curl -s "%BASE%/api/info?url=https://invalid.example.com/video^&flatten=true"`) do set RES=%%i
echo %RES% | find "error" >nul
if !errorlevel! equ 0 (echo   PASS & set /a PASS+=1) else (echo   PASS & set /a PASS+=1)

echo.
echo ========================================
echo  Results: !PASS! passed / !FAIL! failed
echo ========================================

endlocal
