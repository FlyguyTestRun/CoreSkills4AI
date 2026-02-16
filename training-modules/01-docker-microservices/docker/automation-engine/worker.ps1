#!/usr/bin/env pwsh
# Redis job queue worker for PowerShell automation

Import-Module /automation/modules/KISDIdentity.psm1 -Force

Write-Host "Starting Redis job worker..." -ForegroundColor Green

# Simple Redis polling worker
while ($true) {
    try {
        # Check Redis for jobs (using redis-cli in container)
        $jobKey = & redis-cli -h redis LPOP job_queue 2>$null

        if ($jobKey) {
            Write-Host "Processing job: $jobKey" -ForegroundColor Cyan

            # Get job data
            $jobData = & redis-cli -h redis GET $jobKey | ConvertFrom-Json

            if ($jobData.type -eq 'create_student') {
                $result = New-KISDStudentAccount `
                    -StudentID $jobData.data.student_id `
                    -FirstName $jobData.data.first_name `
                    -LastName $jobData.data.last_name `
                    -GradeLevel $jobData.data.grade_level `
                    -GraduationYear $jobData.data.graduation_year

                # Update job status - use Add-Member for new properties
                $jobData.status = 'completed'
                $jobData | Add-Member -NotePropertyName 'result' -NotePropertyValue $result -Force
                $jobData | Add-Member -NotePropertyName 'completed_at' -NotePropertyValue (Get-Date -Format 'o') -Force

                & redis-cli -h redis SET $jobKey ($jobData | ConvertTo-Json -Compress)
                Write-Host "✓ Job completed" -ForegroundColor Green
            }
        }

        Start-Sleep -Seconds 2
    }
    catch {
        Write-Error "Worker error: $_"
        Start-Sleep -Seconds 5
    }
}
