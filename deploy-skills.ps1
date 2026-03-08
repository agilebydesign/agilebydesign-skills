# deploy-skills.ps1
# Creates junctions in the global user skills folder for every skill in this repo.
# Run this once after cloning, and again whenever you add a new skill.
#
# Other workspaces can reference skills via the global path, e.g.:
#   "C:\Users\thoma\.agents\skills\abd-story-synthesizer"
#
# Usage: .\deploy-skills.ps1
#        .\deploy-skills.ps1 -GlobalSkillsPath "C:\some\other\path"

param(
    [string]$GlobalSkillsPath = "C:\Users\thoma\.agents\skills"
)

$canonical = "$PSScriptRoot\skills"

if (-not (Test-Path $canonical)) {
    Write-Host "ERROR: Skills folder not found: $canonical" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $GlobalSkillsPath)) {
    New-Item -ItemType Directory -Path $GlobalSkillsPath -Force | Out-Null
    Write-Host "Created global skills folder: $GlobalSkillsPath" -ForegroundColor Yellow
}

$skills = Get-ChildItem $canonical -Directory
$deployed = 0
$skipped = 0
$replaced = 0

foreach ($skill in $skills) {
    $target = $skill.FullName
    $link   = Join-Path $GlobalSkillsPath $skill.Name

    if (Test-Path $link) {
        $existing = Get-Item $link -Force
        if ($existing.LinkType -eq "Junction") {
            if ($existing.Target -eq $target) {
                Write-Host "  [OK]      $($skill.Name) -> already linked" -ForegroundColor DarkGray
                $skipped++
                continue
            } else {
                # Wrong target — update it
                Remove-Item $link -Force -Recurse
                Write-Host "  [UPDATE]  $($skill.Name) -> re-linking to canonical" -ForegroundColor Yellow
                $replaced++
            }
        } else {
            # Real folder exists — back it up
            $backup = "$link`_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Rename-Item $link $backup
            Write-Host "  [BACKUP]  $($skill.Name) -> backed up real folder to $backup" -ForegroundColor Cyan
            $replaced++
        }
    } else {
        $deployed++
    }

    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Host "  [LINKED]  $($skill.Name)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done: $deployed new, $replaced updated, $skipped already correct" -ForegroundColor Cyan
Write-Host "Global skills folder: $GlobalSkillsPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Other workspaces can reference skills via:" -ForegroundColor DarkGray
foreach ($skill in $skills) {
    Write-Host "  $GlobalSkillsPath\$($skill.Name)" -ForegroundColor DarkGray
}
