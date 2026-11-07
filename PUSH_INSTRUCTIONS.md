# Git Push Instructions - SSH Key Method

## **Your SSH Key Details**

**Private Key:** `C:\Users\Abanob\.ssh\id_ed25519`
**Public Key:** `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDRUVyzZB8F4TcqMsJbFWS1f/2j2h59W6H1Gf703uXV4`

---

## **Step 1: Add SSH Key to ssh-agent (PowerShell)**

Open PowerShell and run:

```powershell
# Start ssh-agent
Start-Service ssh-agent -ErrorAction SilentlyContinue

# Add your private key
ssh-add ~/.ssh/id_ed25519
```

If you get an error about the key format, try:
```powershell
# Set proper permissions
icacls ~/.ssh/id_ed25519 /grant "$env:USERNAME":(OI)(CI)(F)

# Then add key again
ssh-add ~/.ssh/id_ed25519
```

---

## **Step 2: Add Public Key to GitHub (Web Browser)**

1. **Copy your public key:**
   ```powershell
   Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
   ```

2. **Go to GitHub:**
   - Navigate to: https://github.com/settings/keys
   - Or: Click your profile picture → Settings → SSH and GPG keys → New SSH key

3. **Paste and add:**
   - Title: "Windows PC" or "Development"
   - Key: Paste the public key content
   - Click "Add SSH key"
   - You may need to complete 2FA

---

## **Step 3: Push Repository**

```powershell
# From your project directory
cd "C:\Users\Abanob\If I Am Not Embarrassed, Others Will"

# Set remote (if not already set)
git remote add origin git@github.com:aigirl18yearsold/If-I-am-not-embarrassed-others-will-.git

# Set branch and push
git branch -M main
git push -u origin main
```

---

## **Step 4: Verify**

```powershell
# Check connection
ssh -T git@github.com

# Expected output:
# Hi username! You've successfully authenticated, but GitHub does not
# provide shell access.
```

---

## **Alternative: HTTPS with Personal Access Token (PAT)**

If SSH doesn't work, use HTTPS instead:

```powershell
# Generate a PAT at: https://github.com/settings/tokens
# Select scopes: repo, read:admin

# Then push using HTTPS:
cd "C:\Users\Abanob\If I Am Not Embarrassed, Others Will"
git remote add origin https://github.com/aigirl18yearsold/If-I-am-not-embarrassed-others-will-.git
git branch -M main
git push -u origin main
# Enter your GitHub username and PAT when prompted
```

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| `Permission denied (publickey)` | Ensure ssh-agent is running and key is added |
| `Key not authenticated` | Complete 2FA on GitHub after adding key |
| `Invalid key format` | Verify key files are correct, try regenerating |
| `Host key verification failed` | Answer `yes` the first time, or add to known_hosts |

---

## **Current Repository Status**

```
Commits: 2
- a99ec7d: Add world system (Living/Shadow Kingdoms, territories, SHIFT)
- 034a396: Initial project structure
```

**Files ready to push:**
- `.gitignore`, `README.md`, `main.py`, `pyproject.toml`, `src/__init__.py`, `src/scripts/world.py`

---

## **Quick Test**

Run this PowerShell command to verify your SSH key works:

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | clipb oad
# Then visit: https://github.com/settings/keys and add it
```

---

**Need help?** Let me know if you encounter any issues, and I can guide you through specific troubleshooting steps!