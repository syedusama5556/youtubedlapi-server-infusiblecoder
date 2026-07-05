$base = "http://localhost:9192"
$tests = @(
    @{url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; label = "YouTube"},
    @{url = "https://vimeo.com/148751763"; label = "Vimeo"},
    @{url = "https://www.ted.com/talks/ken_robinson_do_schools_kill_creativity"; label = "TED"},
    @{url = "https://www.dailymotion.com/video/xal2ebm"; label = "Dailymotion"},
    @{url = "https://www.instagram.com/p/CxYzE1CRvvF/"; label = "Instagram"},
    @{url = "https://www.tiktok.com/@charlidamelio/video/6829267836786986246"; label = "TikTok"},
    @{url = "https://twitter.com/BarackObama/status/1392062189764227072"; label = "Twitter"},
    @{url = "https://www.twitch.tv/clips/CuteSpunkyDunlinPMST1"; label = "Twitch"},
    @{url = "https://soundcloud.com/bbcsoundwaves/soundwave-1"; label = "SoundCloud"},
    @{url = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"; label = "Spotify"},
    @{url = "https://www.facebook.com/bbcnews/videos/10155596365177857/"; label = "Facebook"}
)

foreach ($t in $tests) {
    Write-Host -NoNewline "$($t.label)... "
    try {
        $r = Invoke-WebRequest -Uri "$base/api/info?url=$([System.Uri]::EscapeDataString($t.url))&flatten=true" -UseBasicParsing -TimeoutSec 45
        $c = $r.Content | ConvertFrom-Json
        if ($c.videos -and $c.videos[0].title) {
            Write-Host "PASS - $($c.videos[0].title.Substring(0, [Math]::Min(60, $c.videos[0].title.Length)))" -ForegroundColor Green
        } else {
            Write-Host "PASS (no title)" -ForegroundColor Green
        }
    } catch {
        try {
            $_.Exception.Response.GetResponseStream().Seek(0,0)
            $body = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream()).ReadToEnd()
            Write-Host "FAIL" -ForegroundColor Red
            Write-Host "  $body"
        } catch {
            Write-Host "FAIL" -ForegroundColor Red
            Write-Host "  $($_.Exception.Message)"
        }
    }
}
