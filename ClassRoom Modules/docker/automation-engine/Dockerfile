# PowerShell automation engine container
FROM mcr.microsoft.com/powershell:lts-alpine-3.20

WORKDIR /automation

# Install redis-cli
RUN apk add --no-cache redis

# Install PowerShell modules
RUN pwsh -Command "Install-Module -Name PSFramework -Force -Scope AllUsers"

# Copy PowerShell modules and worker
COPY modules/ ./modules/
COPY entrypoint.ps1 worker.ps1 ./

RUN chmod +x entrypoint.ps1 worker.ps1

CMD ["pwsh", "./worker.ps1"]
