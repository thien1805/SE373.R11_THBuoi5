Set-Location "d:\Download\agent-tools-skills-lab"
$git = "C:\Program Files\Microsoft SQL Server Management Studio 21\Release\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\Git\cmd\git.exe"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   DANG PUSH MA NGUON LEN GITHUB (SE373.R11_THBuoi5)   " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
& $git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nThu push bang --force..." -ForegroundColor Yellow
    & $git push -u origin main --force
}
