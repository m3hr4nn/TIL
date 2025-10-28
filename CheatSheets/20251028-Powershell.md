# PowerShell Interview Cheat Sheet

## Basic Concepts

### Cmdlet Structure
```powershell
Verb-Noun -Parameter Value
Get-Process -Name chrome
```

**Common Verbs:** Get, Set, New, Remove, Add, Clear, Start, Stop, Restart, Test

### Getting Help
```powershell
Get-Help Get-Process
Get-Help Get-Process -Examples
Get-Help Get-Process -Full
Get-Help *service*              # Search commands
Get-Command *process*           # Find commands
Get-Member                      # Object properties/methods
```

## Variables & Data Types

### Variables
```powershell
$variable = "value"
$number = 42
$array = @(1, 2, 3, 4)
$hashtable = @{Name='John'; Age=30}
[string]$typed = "forced type"

# Special Variables
$PSVersionTable                 # PowerShell version
$Error[0]                       # Last error
$_                              # Current pipeline object
$?                              # Last command success (true/false)
$Args                           # Script arguments
$env:PATH                       # Environment variables
```

### Data Types
```powershell
[int]$num = 42
[string]$text = "hello"
[array]$arr = @(1,2,3)
[hashtable]$hash = @{}
[datetime]$date = Get-Date
[bool]$flag = $true
```

## File System Operations

### Navigation & Manipulation
```powershell
Get-Location                    # Current directory (pwd)
Set-Location C:\path            # Change directory (cd)
Get-ChildItem                   # List items (ls, dir)
Get-ChildItem -Recurse          # Recursive listing
Get-ChildItem -Filter "*.txt"   # Filter by extension

New-Item file.txt -ItemType File
New-Item folder -ItemType Directory
Copy-Item source dest
Move-Item old new
Remove-Item file.txt
Remove-Item folder -Recurse -Force

Test-Path C:\file.txt           # Check if exists
```

### File Content
```powershell
Get-Content file.txt            # Read file
Get-Content file.txt | Select-Object -First 10  # First 10 lines
Set-Content file.txt "text"     # Write (overwrite)
Add-Content file.txt "text"     # Append
Clear-Content file.txt          # Empty file
```

## Working with Objects

### Pipeline & Object Filtering
```powershell
Get-Process | Where-Object {$_.CPU -gt 10}
Get-Process | Where-Object CPU -gt 10  # Simplified syntax
Get-Service | Where-Object Status -eq "Running"

# Select specific properties
Get-Process | Select-Object Name, CPU, Id

# Sort objects
Get-Process | Sort-Object CPU -Descending

# Group objects
Get-Service | Group-Object Status

# Measure objects
Get-Process | Measure-Object -Property CPU -Sum
```

### ForEach and Loops
```powershell
# ForEach-Object (pipeline)
Get-Service | ForEach-Object {
    Write-Host $_.Name
}

# foreach statement
$items = 1..5
foreach ($item in $items) {
    Write-Host $item
}

# For loop
for ($i = 0; $i -lt 5; $i++) {
    Write-Host $i
}

# While loop
$i = 0
while ($i -lt 5) {
    Write-Host $i
    $i++
}
```

## Conditionals

### If Statements
```powershell
if ($condition) {
    # code
} elseif ($condition) {
    # code
} else {
    # code
}

# Comparison operators
-eq                             # Equal
-ne                             # Not equal
-gt                             # Greater than
-lt                             # Less than
-ge                             # Greater or equal
-le                             # Less or equal
-like                           # Wildcard match
-match                          # Regex match
-contains                       # Collection contains
-in                             # Item in collection
```

### Switch Statement
```powershell
switch ($value) {
    1 { "One" }
    2 { "Two" }
    default { "Other" }
}
```

## Functions

### Basic Function
```powershell
function Get-Greeting {
    param(
        [string]$Name = "World"
    )
    return "Hello, $Name!"
}

Get-Greeting -Name "John"
```

### Advanced Function
```powershell
function Get-Data {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Path,
        
        [Parameter(Mandatory=$false)]
        [switch]$Recurse
    )
    
    process {
        if (Test-Path $Path) {
            Get-ChildItem $Path -Recurse:$Recurse
        }
    }
}
```

## Process Management

### Process Commands
```powershell
Get-Process                     # List all processes
Get-Process -Name chrome        # Specific process
Stop-Process -Name notepad      # Kill process
Stop-Process -Id 1234 -Force    # Kill by PID
Start-Process notepad           # Start process
Start-Process "app.exe" -Verb RunAs  # Run as admin

# Services
Get-Service
Get-Service -Name wuauserv
Start-Service -Name wuauserv
Stop-Service -Name wuauserv
Restart-Service -Name wuauserv
Set-Service -Name wuauserv -StartupType Automatic
```

## Remote Management

### PowerShell Remoting
```powershell
# Enable remoting
Enable-PSRemoting -Force

# One-to-One remoting
Enter-PSSession -ComputerName Server01
Exit-PSSession

# One-to-Many remoting
Invoke-Command -ComputerName Server01,Server02 -ScriptBlock {
    Get-Process
}

# Persistent session
$session = New-PSSession -ComputerName Server01
Invoke-Command -Session $session -ScriptBlock { Get-Service }
Remove-PSSession $session

# Copy files to remote
Copy-Item -Path C:\file.txt -Destination C:\remote\ -ToSession $session
```

## Working with CSV/JSON/XML

### CSV Operations
```powershell
# Import CSV
$data = Import-Csv data.csv
$data | Where-Object Age -gt 30

# Export CSV
Get-Process | Export-Csv processes.csv -NoTypeInformation
```

### JSON Operations
```powershell
# Convert to JSON
$object | ConvertTo-Json -Depth 3

# Parse JSON
$json = Get-Content data.json | ConvertFrom-Json
```

### XML Operations
```powershell
[xml]$xml = Get-Content file.xml
$xml.root.element
```

## Error Handling

### Try-Catch-Finally
```powershell
try {
    # Code that might fail
    Get-Item "C:\nonexistent.txt" -ErrorAction Stop
} catch {
    Write-Host "Error: $_"
    Write-Host $_.Exception.Message
} finally {
    # Always executes
    Write-Host "Cleanup"
}
```

### Error Action Preference
```powershell
$ErrorActionPreference = "Stop"        # Stops on error
$ErrorActionPreference = "Continue"    # Default
$ErrorActionPreference = "SilentlyContinue"  # Suppress errors

# Per command
Get-Process -Name fake -ErrorAction SilentlyContinue
```

## Registry Operations

```powershell
# Navigate registry
Set-Location HKLM:\Software

# Get registry value
Get-ItemProperty -Path "HKLM:\Software\Microsoft"

# Set registry value
New-ItemProperty -Path "HKLM:\Software\MyApp" -Name "Setting" -Value "Value"
Set-ItemProperty -Path "HKLM:\Software\MyApp" -Name "Setting" -Value "NewValue"

# Remove registry item
Remove-Item -Path "HKLM:\Software\MyApp" -Recurse
```

## Active Directory (if AD module available)

```powershell
Import-Module ActiveDirectory

# Get user
Get-ADUser -Identity jdoe
Get-ADUser -Filter {Name -like "*John*"}

# Get group members
Get-ADGroupMember -Identity "Domain Admins"

# Create user
New-ADUser -Name "John Doe" -SamAccountName jdoe

# Modify user
Set-ADUser -Identity jdoe -EmailAddress "jdoe@company.com"
```

## String Manipulation

```powershell
$text = "Hello World"
$text.Length                    # String length
$text.ToUpper()                 # HELLO WORLD
$text.ToLower()                 # hello world
$text.Substring(0, 5)           # Hello
$text.Replace("World", "PS")    # Hello PS
$text.Split(" ")                # Array: Hello, World
$text.Contains("World")         # True
$text.StartsWith("Hello")       # True
$text -match "W\w+"             # Regex match

# String formatting
"Name: {0}, Age: {1}" -f $name, $age
"Name: $name, Age: $age"        # Variable interpolation
```

## Execution Policy

```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned
Set-ExecutionPolicy Bypass -Scope Process

# Execution Policies:
# Restricted - No scripts
# AllSigned - Only signed scripts
# RemoteSigned - Local scripts + signed remote
# Unrestricted - All scripts with warning
# Bypass - Nothing blocked, no warnings
```

## Common Interview Questions

**Q: What is the difference between PowerShell and CMD?**
- PowerShell is object-based, CMD is text-based
- PowerShell has cmdlets, CMD has commands
- PowerShell supports pipeline for objects, not just text
- PowerShell has advanced scripting capabilities

**Q: What are PowerShell Profiles?**
- Scripts that run when PowerShell starts
- `$PROFILE` - Current user, current host
- Use for aliases, functions, environment setup

**Q: Difference between `-eq` and `==`?**
- PowerShell uses `-eq`, not `==`
- `-eq` is the equality operator

**Q: What is `$_` or `$PSItem`?**
- Current object in pipeline
- Used in `Where-Object`, `ForEach-Object`

**Q: What is splatting?**
```powershell
$params = @{
    Name = 'process'
    ComputerName = 'Server01'
}
Get-Process @params
```

**Q: How to run script as administrator?**
```powershell
Start-Process powershell -Verb RunAs -ArgumentList "-File script.ps1"
```

**Q: Difference between `Get-Member` and `Get-Command`?**
- `Get-Member` shows properties/methods of objects
- `Get-Command` lists available commands

**Q: What are PowerShell modules?**
- Packages of cmdlets, functions, variables
- `Get-Module -ListAvailable`
- `Import-Module ModuleName`
