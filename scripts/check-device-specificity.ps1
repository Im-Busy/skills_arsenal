# scripts/check-device-specificity.ps1
# Scans the arsenal for hardcoded device-specific paths (C:\Dev\), Windows-specific paths,
# and other device-specific patterns. Exit 0 = no device-specific FAIL findings.
#
# Exit codes: 0=no device-specific FAILs, 1=FAILs found

param(
    [string]$SkillName
)

$ErrorActionPreference = "Continue"
$ArsenalRoot = Split-Path $PSScriptRoot -Parent  # project root (parent of scripts/)

# ---- Patterns that indicate device-specificity ----
# FAIL patterns (absolute paths / hardcoded usernames)
$FailPatterns = @(
    @{ Name = "abs_dev_d";      Pattern = '(?i)\bC:\\Dev\\';              Reason = "Hardcoded C:\Dev\ absolute path" },
    @{ Name = "abs_unix_home";  Pattern = '(?i)/home/[a-zA-Z][a-zA-Z0-9_-]*'; Reason = "Hardcoded Unix home path" },
    @{ Name = "abs_mac_home";   Pattern = '(?i)/Users/[a-zA-Z][a-zA-Z0-9_-]*'; Reason = "Hardcoded macOS home path" },
    @{ Name = "abs_win_user";   Pattern = '(?i)[A-Z]:\\Users\\[^\\]+\\';  Reason = "Hardcoded Windows user profile path" },
    @{ Name = "abs_win_prog";   Pattern = '(?i)\bC:\\Program Files';       Reason = "Hardcoded Program Files path" }
)

# WARN patterns (localhost references - generally acceptable in dev docs)
$WarnPatterns = @(
    @{ Name = "localhost_loopback"; Pattern = '127\.0\.0\.1';           Reason = "Localhost loopback address" },
    @{ Name = "localhost";          Pattern = '(?i)\blocalhost\b';      Reason = "localhost reference" },
    @{ Name = "private_10";         Pattern = '(?i)\b10\.0\.0\.\d+\b';  Reason = "RFC1918 private address" },
    @{ Name = "abs_dotenv";         Pattern = '(?i)\.env\b';             Reason = ".env reference (not an absolute path)" }
)

# Skills to skip entirely
$SkipDirs = @(
    'deepscientist-windows-wsl-setup'  # intentionally Windows-specific
)

function Scan-File($FilePath, $RelPath) {
    $content = Get-Content $FilePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $content) { return @() }

    $findings = @()
    foreach ($p in $FailPatterns) {
        $matches = [regex]::Matches($content, $p.Pattern)
        if ($matches.Count -gt 0) {
            # Filter: skip matches that are inside a URL (preceded by http:// or https://)
            $realMatches = $matches | Where-Object {
                $idx = $_.Index
                # Check if this match is inside a URL: look back for '://' within 60 chars
                $windowStart = [Math]::Max(0, $idx - 60)
                $preceding = $content.Substring($windowStart, $idx - $windowStart)
                ($preceding -notmatch 'https?://')
            }
            if ($realMatches.Count -gt 0) {
                $samples = $realMatches | Select-Object -First 3 | ForEach-Object { $_.Value }
                $findings += [PSCustomObject]@{
                    PatternId = $p.Name
                    Severity  = "FAIL"
                    Count     = $realMatches.Count
                    Samples   = $samples
                    File      = $RelPath
                }
            }
        }
    }
    foreach ($p in $WarnPatterns) {
        $matches = [regex]::Matches($content, $p.Pattern)
        if ($matches.Count -gt 0) {
            # Filter: skip matches that are inside a URL
            $realMatches = $matches | Where-Object {
                $idx = $_.Index
                $windowStart = [Math]::Max(0, $idx - 60)
                $preceding = $content.Substring($windowStart, $idx - $windowStart)
                ($preceding -notmatch 'https?://')
            }
            if ($realMatches.Count -gt 0) {
                $samples = $realMatches | Select-Object -First 3 | ForEach-Object { $_.Value }
                $findings += [PSCustomObject]@{
                    PatternId = $p.Name
                    Severity  = "WARN"
                    Count     = $realMatches.Count
                    Samples   = $samples
                    File      = $RelPath
                }
            }
        }
    }
    return $findings
}

# ---- Main ----

Write-Host "Device-Specificity Check" -ForegroundColor Cyan
Write-Host "Root: $ArsenalRoot" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan
Write-Host ""

$universalRoot = Join-Path $ArsenalRoot "universal-skills"
$domainRoot    = Join-Path $ArsenalRoot "domain-specific-skills"

$mdFiles = @()
if (Test-Path $universalRoot) {
    $mdFiles += Get-ChildItem -Path $universalRoot -Include "*.md" -Recurse -File -ErrorAction SilentlyContinue
}
if (Test-Path $domainRoot) {
    $mdFiles += Get-ChildItem -Path $domainRoot -Include "*.md" -Recurse -File -ErrorAction SilentlyContinue
}

if ($SkillName) {
    $want = $SkillName.Replace('\', '/')
    $mdFiles = $mdFiles | Where-Object {
        $rel = $_.FullName.Substring($ArsenalRoot.Length).TrimStart('\', '/').Replace('\', '/')
        ($rel -eq $want) -or ($_.Directory.Name -eq $want) -or ($rel -like "*/$want")
    }
}

$allFindings = @()
$filesScanned = 0

foreach ($file in $mdFiles) {
    # Skip intentionally device-specific skills
    $rel = $file.FullName.Substring($ArsenalRoot.Length).TrimStart('\', '/').Replace('\', '/')
    if ($SkipDirs | Where-Object { $rel -like "*$_*" }) { continue }

    $filesScanned++
    $findings = Scan-File $file.FullName $rel
    $allFindings += $findings
}

$failFindings = $allFindings | Where-Object { $_.Severity -eq "FAIL" }
$warnFindings = $allFindings | Where-Object { $_.Severity -eq "WARN" }

# Report
Write-Host "Files scanned: $filesScanned" -ForegroundColor DarkGray
Write-Host "FAIL findings: $($failFindings.Count)" -ForegroundColor $(if ($failFindings.Count -gt 0) { "Red" } else { "Green" })
Write-Host "WARN findings: $($warnFindings.Count)" -ForegroundColor $(if ($warnFindings.Count -gt 0) { "Yellow" } else { "DarkGray" })
Write-Host ""

if ($failFindings) {
    Write-Host "FAIL findings:" -ForegroundColor Red
    foreach ($f in $failFindings) {
        Write-Host "  [$($f.PatternId)] $($f.File)" -ForegroundColor Red
        Write-Host "    Count: $($f.Count)  Samples: $($f.Samples -join ', ')" -ForegroundColor DarkGray
    }
}

if ($warnFindings) {
    Write-Host "WARN findings (informational):" -ForegroundColor Yellow
    foreach ($f in $warnFindings | Group-Object PatternId | Select-Object -First 10) {
        $sample = ($warnFindings | Where-Object { $_.PatternId -eq $f.Name } | Select-Object -First 1).Samples[0]
        Write-Host "  [$($f.Name)] $($f.Count) occurrences — sample: $sample" -ForegroundColor DarkGray
    }
}

if ($failFindings.Count -eq 0) {
    Write-Host ""
    Write-Host "No device-specific FAIL findings." -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "Device-specific FAILs found — fix before publishing." -ForegroundColor Red
    exit 1
}
