# 🧠 CP Client - API Script

This Python script (`cp_api_client.py`) is a lightweight client to interact with the **Code Preceptor API** — providing various developer tools such as URL shortening, IP lookup, hash generation, and more.

---

## 🚀 Features

- 🔐 Token-based authentication
- 🔗 Shorten and manage URLs
- 🌍 IP Geolocation lookup
- 🧠 User-Agent analysis
- 🧮 Base64 encode/decode
- 🔐 MD5, SHA256, and SHA512 hash generation
- 📊 Future-ready for usage analytics

---

## 📦 Requirements

- Python 3.6 or above
- `requests` library (install with pip)

```bash
pip install requests

---

📄 Usage Section

## 💡 How to Use

Run the script from your terminal:

```bash
python cp_api_client.py
'''
You'll be prompted to:

Select an action (e.g., shorten a URL, lookup IP, etc.)

Enter the required input

View the response from the API


---

### 🔐 Security Advice Section
```markdown
## 🔐 Security Advice

- Never share your `.cp_config.json` file or API key publicly.
- Use environment-specific keys for production and testing.
- If your key is compromised, revoke and regenerate it from your account dashboard.


---

🧑‍💻 Author Section

## 🧑‍💻 Author

**Code Preceptor**  
💻 [https://codepreceptor.tech](https://codepreceptor.tech)


---

⚙️ How to Use (Expanded with Setup and Run)

## ⚙️ Setup

1. **Clone this repository:**

```bash
git clone https://github.com/codepreceptor/cp-client.git
cd cp-client

2. Create a .cp_config.json file:



{
  "api_url": "https://your-api-url.com",
  "api_key": "your_api_token_here"
}

> ⚠️ This file is private and is excluded from version control using .gitignore.




---

💡 How to Use

Run the script from your terminal:

python cp_api_client.py

You'll be prompted to:

Select an action (e.g., shorten a URL, lookup IP, etc.)

Enter the required input

View the response from the API


---

If you want, I can provide all these combined in a single block or help with any other README section!

