# scripts/audit-arsenal.ps1
# Audits all SKILL.md files in skills_arsenal_for_publishing for structural validity.
# Adapted from C:\Dev\scripts\audit-skills.ps1
#
# Exit codes: 0=all pass, 1=warnings, 2=errors

param(
    [string]$SkillName
)

$ErrorActionPreference = "Continue"
$ArsenalRoot = Split-Path $PSScriptRoot -Parent  # project root (parent of scripts/)

# ---- YAML Frontmatter Parser ----

function Extract-Frontmatter($FilePath) {
    $content = Get-Content $FilePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $content) { return $null }

    if ($content -notmatch '(?s)^---\s*\n(.*?)\n---') {
        return $null
    }
    $block = $Matches[1]

    $result = @{}
    $inDesc = $false
    $inMeta = $false
    $descLines = @()

    foreach ($line in ($block -split '\r?\n')) {
        if ($line -match '^\s*description\s*:\s*>\s*$') {
            $inDesc = $true
            continue
        }

        if ($inDesc) {
            if ($line -match '^\S') {
                $result['description'] = ($descLines -join ' ').Trim()
                $descLines = @()
                $inDesc = $false
            } else {
                $descLines += $line.Trim()
                continue
            }
        }

        if ($line -match '^\s*metadata\s*:\s*$') {
            $inMeta = $true
            $result['metadata'] = @{}
            continue
        }

        if ($inMeta) {
            if ($line -match '^\s{2,}(\w[\w-]*)\s*:\s*(.*)') {
                $mk = $Matches[1]
                $mv = $Matches[2].Trim().Trim('"').Trim("'")
                $result['metadata'][$mk] = $mv
                continue
            } elseif ($line -match '^\S') {
                $inMeta = $false
            } else {
                continue
            }
        }

        if ($line -match '^(\w[\w-]*)\s*:\s*(.*)') {
            $key = $Matches[1]
            $val = $Matches[2].Trim().Trim('"').Trim("'")
            $result[$key] = $val
        }
    }

    if ($inDesc -and $descLines.Count -gt 0) {
        $result['description'] = ($descLines -join ' ').Trim()
    }

    return $result
}

# ---- Validators ----

function Is-ValidPosture($p) {
    return $p -in @('hybrid', 'auto-first', 'manual-first', 'reference')
}

function Is-SemVer($v) {
    return $v -match '^\d+\.\d+\.\d+$'
}

# ---- Main ----

Write-Host "Arsenal Skill Audit" -ForegroundColor Cyan
Write-Host "Root: $ArsenalRoot" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan
Write-Host ""

# Find all SKILL.md in universal-skills/ and domain-specific-skills/
$universalRoot = Join-Path $ArsenalRoot "universal-skills"
$domainRoot    = Join-Path $ArsenalRoot "domain-specific-skills"

$skillDirs = @()
if (Test-Path $universalRoot) {
    $skillDirs += Get-ChildItem -Path $universalRoot -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }
}
if (Test-Path $domainRoot) {
    $skillDirs += Get-ChildItem -Path $domainRoot -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName "SKILL.md") }
}

if ($SkillName) {
    $want = $SkillName.Replace('\', '/')
    $skillDirs = $skillDirs | Where-Object {
        $rel = $_.FullName.Substring($ArsenalRoot.Length).TrimStart('\', '/').Replace('\', '/')
        ($rel -eq $want) -or ($_.Name -eq $want) -or ($rel -like "*/$want")
    }
    if (-not $skillDirs) {
        Write-Host "Skill '$SkillName' not found." -ForegroundColor Red
        exit 2
    }
}

if (-not $skillDirs) {
    Write-Host "No skills with SKILL.md found." -ForegroundColor Yellow
    exit 1
}

# Analyze each skill
$results = @()
$totalFail = 0
$totalWarn = 0
$totalPass = 0

foreach ($dir in $skillDirs) {
    $relPath = $dir.FullName.Substring($ArsenalRoot.Length).TrimStart('\', '/').Replace('\', '/')
    $leaf = $dir.Name
    $mdPath = Join-Path $dir.FullName "SKILL.md"
    $jsonPath = Join-Path $dir.FullName "skill.json"

    $issues = @()
    $warns = @()
    $posture = "?"
    $ver = "?"
    $status = "PASS"

    $fm = Extract-Frontmatter $mdPath

    if (-not $fm) {
        $issues += "No YAML frontmatter"
        $status = "FAIL"
    } else {
        # name
        $fmName = $fm['name']
        if (-not $fmName) {
            $issues += "name missing"
        } elseif (($fmName -ne $relPath) -and ($fmName -ne $leaf)) {
            $warns += "name '$fmName' != dir '$relPath'"
        }

        # description
        $desc = ""
        if ($fm['description']) { $desc = $fm['description'].ToString().Trim() }
        if ($desc.Length -eq 0) {
            $issues += "description missing"
        }

        # version (top-level or metadata.version)
        $ver = $fm['version']
        if (-not $ver -and $fm['metadata'] -is [hashtable]) {
            $ver = $fm['metadata']['version']
        }
        if (-not $ver) {
            $warns += "version missing"
            $ver = "?"
        } elseif (-not (Is-SemVer $ver)) {
            $issues += "version '$ver' not semver"
        }

        # license
        if (-not $fm['license']) {
            $warns += "license missing"
        }

        # posture
        if ($fm['metadata'] -is [hashtable]) {
            $mp = $fm['metadata']['invocation_posture']
            if ($mp) { $posture = $mp }
        }
        if (-not (Is-ValidPosture $posture)) {
            $issues += "posture missing or invalid ('$posture')"
        }

        # skill.json
        if (Test-Path $jsonPath) {
            try {
                $sj = Get-Content $jsonPath -Raw | ConvertFrom-Json
                if ($sj.name -and ($sj.name -ne $relPath) -and ($sj.name -ne $leaf)) {
                    $warns += "skill.json name '$($sj.name)' != dir '$relPath'"
                }
                $jp = $sj.invocation_posture
                if ($jp -and $jp -ne $posture) {
                    $warns += "posture: md='$posture' vs json='$jp'"
                }
            } catch {
                $warns += "skill.json parse error"
            }
        } else {
            $warns += "skill.json missing"
        }
    }

    if ($issues.Count -gt 0) {
        $status = "FAIL"
        $totalFail++
    } elseif ($warns.Count -gt 0) {
        $status = "WARN"
        $totalWarn++
    } else {
        $totalPass++
    }

    $allMsgs = $issues + ($warns | ForEach-Object { "[w] $_" })
    $msgStr = if ($allMsgs.Count -gt 0) { ($allMsgs -join '; ') } else { "-" }

    $results += [PSCustomObject]@{
        Name   = $relPath
        Posture = $posture
        Version = $ver
        Status  = $status
        Issues  = $msgStr
    }
}

# Output
$fmt = "{0,-50} {1,-14} {2,-8} {3}"
Write-Host ($fmt -f "SKILL", "POSTURE", "VERSION", "ISSUES") -ForegroundColor White
Write-Host ($fmt -f "-----", "-------", "-------", "------") -ForegroundColor DarkGray

foreach ($r in ($results | Sort-Object Name)) {
    $c = switch ($r.Status) {
        "PASS" { "Green" }
        "WARN" { "Yellow" }
        "FAIL" { "Red" }
        default { "White" }
    }
    $dispName = $r.Name
    if ($dispName.Length -gt 50) { $dispName = $dispName.Substring(0, 47) + "..." }
    Write-Host ($fmt -f $dispName, $r.Posture, $r.Version, "$($r.Status): $($r.Issues)") -ForegroundColor $c
}

# Summary
Write-Host ""
$sumColor = if ($totalFail -gt 0) { "Red" } elseif ($totalWarn -gt 0) { "Yellow" } else { "Green" }
Write-Host "Total: $($results.Count) | PASS: $totalPass | WARN: $totalWarn | FAIL: $totalFail" -ForegroundColor $sumColor

if ($totalFail -eq 0 -and $totalWarn -eq 0) {
    Write-Host "All skills valid. No issues." -ForegroundColor Green
    exit 0
} elseif ($totalFail -gt 0) {
    exit 2
} else {
    exit 1
}
