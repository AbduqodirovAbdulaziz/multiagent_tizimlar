# GitHub'ga Yuklash Qo'llanmasi

**Repository:** https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git  
**Sana:** 12-May, 2026

---

## 🚀 Qadamma-Qadam Qo'llanma

### 1. Git Repository Initsializatsiya

```bash
# Git repository yaratish
git init

# Git config (agar sozlanmagan bo'lsa)
git config user.name "AbduqodirovAbdulaziz"
git config user.email "your-email@example.com"
```

### 2. .gitignore Tekshirish

`.gitignore` fayli allaqachon mavjud va to'g'ri sozlangan:
- ✅ `venv310/` - Virtual environment ignore qilinadi
- ✅ `.env` - Environment variables ignore qilinadi
- ✅ `db.sqlite3` - Database ignore qilinadi
- ✅ `__pycache__/` - Python cache ignore qilinadi
- ✅ `*.pyc` - Compiled Python files ignore qilinadi

### 3. Barcha Fayllarni Qo'shish

```bash
# Barcha fayllarni staging'ga qo'shish
git add .

# Qo'shilgan fayllarni ko'rish
git status
```

**Kutilayotgan natija:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .env.example
        new file:   .gitignore
        new file:   README.md
        new file:   apps/...
        ... (110+ files)
```

### 4. Commit Yaratish

```bash
# Birinchi commit
git commit -m "Initial commit: Complete Medical Multiagent Diagnostic System

- 6 Django apps (core, agents, patients, diagnostics, dashboard, api)
- 5 specialized AI agents with BDI architecture
- FIPA-ACL protocol implementation
- RESTful API with Swagger documentation
- Admin panel with Jazzmin theme
- Complete diagnostic workflow
- Comprehensive documentation
- Ready for deployment"
```

### 5. Remote Repository Qo'shish

```bash
# GitHub repository'ni remote sifatida qo'shish
git remote add origin https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git

# Remote'ni tekshirish
git remote -v
```

**Kutilayotgan natija:**
```
origin  https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git (fetch)
origin  https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git (push)
```

### 6. Branch Nomini O'zgartirish (agar kerak bo'lsa)

```bash
# Asosiy branch'ni main deb nomlash
git branch -M main
```

### 7. GitHub'ga Push Qilish

```bash
# Birinchi marta push qilish
git push -u origin main
```

**Agar xatolik bo'lsa:**

#### Xatolik 1: Repository bo'sh emas
```bash
# Agar GitHub'da allaqachon fayllar bo'lsa
git pull origin main --allow-unrelated-histories
git push -u origin main
```

#### Xatolik 2: Authentication kerak
```bash
# GitHub Personal Access Token kerak
# GitHub.com > Settings > Developer settings > Personal access tokens
# Token yarating va parol o'rniga ishlatilng
```

---

## 📋 To'liq Buyruqlar Ketma-ketligi

```bash
# 1. Git init
git init

# 2. Fayllarni qo'shish
git add .

# 3. Commit
git commit -m "Initial commit: Complete Medical Multiagent Diagnostic System"

# 4. Remote qo'shish
git remote add origin https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git

# 5. Branch nomini o'zgartirish
git branch -M main

# 6. Push qilish
git push -u origin main
```

---

## ✅ Tekshirish

Push qilgandan keyin:

1. **GitHub'da tekshiring:**
   - https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar
   - Barcha fayllar ko'rinishi kerak
   - README.md to'g'ri ko'rsatilishi kerak

2. **Ignore qilingan fayllar:**
   - ❌ `.env` - Ko'rinmasligi kerak
   - ❌ `venv310/` - Ko'rinmasligi kerak
   - ❌ `db.sqlite3` - Ko'rinmasligi kerak
   - ❌ `__pycache__/` - Ko'rinmasligi kerak

3. **Mavjud fayllar:**
   - ✅ `.env.example` - Ko'rinishi kerak
   - ✅ `README.md` - Ko'rinishi kerak
   - ✅ `apps/` - Barcha app'lar
   - ✅ `config/` - Konfiguratsiya
   - ✅ `requirements/` - Dependencies

---

## 🔧 Muammolarni Hal Qilish

### Muammo 1: "fatal: not a git repository"
```bash
# Yechim: Git init qilish
git init
```

### Muammo 2: "remote origin already exists"
```bash
# Yechim: Eski remote'ni o'chirish
git remote remove origin
git remote add origin https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
```

### Muammo 3: "failed to push some refs"
```bash
# Yechim: Pull qilib, keyin push qilish
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Muammo 4: Authentication xatosi
```bash
# Yechim: Personal Access Token yaratish
# 1. GitHub.com > Settings > Developer settings
# 2. Personal access tokens > Tokens (classic)
# 3. Generate new token
# 4. Scope: repo (full control)
# 5. Token'ni nusxalash
# 6. Push qilganda parol o'rniga token ishlatish
```

---

## 📝 Keyingi O'zgarishlar Uchun

Kelajakda o'zgarishlar qilganingizda:

```bash
# 1. O'zgarishlarni ko'rish
git status

# 2. O'zgarishlarni qo'shish
git add .

# 3. Commit
git commit -m "Description of changes"

# 4. Push
git push origin main
```

---

## 🌿 Branch Bilan Ishlash (Optional)

Yangi feature qo'shish uchun:

```bash
# Yangi branch yaratish
git checkout -b feature/new-feature

# O'zgarishlar qilish
git add .
git commit -m "Add new feature"

# GitHub'ga push
git push origin feature/new-feature

# GitHub'da Pull Request yaratish
```

---

## 📊 Repository Sozlamalari

GitHub'da repository sozlamalarini tekshiring:

### 1. Repository Settings
- **Description:** Medical Multiagent Diagnostic Platform
- **Topics:** django, python, multiagent-system, medical, ai, bdi-architecture, fipa-acl
- **Website:** (agar deploy qilsangiz)

### 2. README.md
- ✅ Allaqachon to'liq README.md mavjud
- ✅ Badges qo'shish mumkin (optional)

### 3. License (Optional)
```bash
# MIT License qo'shish
# GitHub'da: Add file > Create new file > LICENSE
# Template: MIT License
```

### 4. .github/ Folder (Optional)
```bash
# Issue templates
# Pull request templates
# GitHub Actions workflows
```

---

## 🎯 Yakuniy Tekshiruv

Push qilgandan keyin quyidagilarni tekshiring:

- [ ] Repository ochiladi
- [ ] README.md to'g'ri ko'rsatiladi
- [ ] Barcha fayllar mavjud
- [ ] .env fayli yo'q (ignore qilingan)
- [ ] venv310/ yo'q (ignore qilingan)
- [ ] db.sqlite3 yo'q (ignore qilingan)
- [ ] Dokumentatsiya fayllari mavjud
- [ ] Code to'g'ri formatlangan

---

## 🚀 Keyingi Qadam: PythonAnywhere

GitHub'ga yuklangandan keyin:

1. **PythonAnywhere'da clone qiling:**
   ```bash
   git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
   ```

2. **Deploy qiling:**
   - `PYTHONANYWHERE_DEPLOYMENT.md` faylini o'qing
   - Qadamma-qadam amal qiling

---

## 💡 Foydali Git Buyruqlari

```bash
# Holat ko'rish
git status

# Log ko'rish
git log --oneline

# O'zgarishlarni ko'rish
git diff

# Oxirgi commit'ni o'zgartirish
git commit --amend

# Branch'lar ro'yxati
git branch -a

# Remote'lar ro'yxati
git remote -v

# Pull (yangilanishlarni olish)
git pull origin main

# Clone (boshqa joyda)
git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
```

---

## 📞 Yordam

Agar muammo bo'lsa:

1. **Git Documentation:** https://git-scm.com/doc
2. **GitHub Guides:** https://guides.github.com/
3. **Stack Overflow:** https://stackoverflow.com/questions/tagged/git

---

**Yaratilgan:** 12-May, 2026  
**Repository:** https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git  
**Holat:** ✅ TAYYOR

**Omad tilaymiz! 🚀**
