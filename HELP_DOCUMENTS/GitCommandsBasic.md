# See what has changed / is staged / is untracked
`git status`
# Short version
`git status --short`

# View commit history (compact and pretty)
`git log --oneline --graph --decorate`
# Even nicer with dates & authors
`git log --oneline --graph --all --decorate --format="%C(yellow)%h%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset"`

# Pull latest changes from remote (before you start working)
`git pull`
# or explicit:
`git pull origin main`

# Undo local changes on a file (careful – permanent!)
`git restore filename.py`
# or older syntax (still works):
`git checkout -- filename.py`

# Unstage a file (remove from index but keep changes)
`git restore --staged filename.py`
# or older:
`git reset HEAD filename.py`

--- 

# Option 1: Double quotes (most common and readable)
`cd "Ideas for Modules"`

# Option 2: Single quotes (also works)
`cd 'Ideas for Modules'`

# Option 3: Escape each space with backtick ` (PowerShell escape character)
`cd Ideas` for` Modules`

# Option 4: Full absolute path (safest when in doubt)
`cd "C:\CoreSkills4ai\ClassRoom Modules\Modules\Ideas for Modules"`
# or escaped:
`cd C:\CoreSkills4ai\ClassRoom` Modules\Modules\Ideas` for` Modules`

--- 
`PS C:\CoreSkills4ai\ClassRoom Modules\Modules\Ideas for Modules>`

---

# If venv folder is named "venv" (most common)
`.\venv\Scripts\Activate.ps1`

# If named ".venv" (popular convention)
`.\.venv\Scripts\Activate.ps1`

# If named "env"
`.\env\Scripts\Activate.ps1`