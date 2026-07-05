$base = "http://localhost:9192"
$tests = @(
    @{url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; label = "YouTube"},
    @{url = "https://vimeo.com/76979871"; label = "Vimeo"},
    @{url = "https://www.ted.com/talks/chloe_valdary_how_love_can_help_repair_social_inequality"; label = "TED"},
    @{url = "https://www.dailymotion.com/video/xal2ebm"; label = "Dailymotion"},
    @{url = "https://www.instagram.com/p/DZum0cIgpUN/"; label = "Instagram"},
    @{url = "https://www.tiktok.com/@natgeo/video/7657545298406935821"; label = "TikTok"},
    @{url = "https://x.com/WhiteHouse/status/2073120924753113295"; label = "Twitter/X"},
    @{url = "https://www.twitch.tv/ninja/clip/ImpartialPiercingAirGuitarRlyTho-XAifq5WBLrORdP1G"; label = "Twitch"},
    @{url = "https://soundcloud.com/vanya-srivastava-369319403"; label = "SoundCloud"},
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
