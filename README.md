# read-my-e-mails
A tool written in python to read aloud only important e-mails summary

We`re receiving too many e-mails, and wasting too much time to read them, so my concept is that computer should download, analyze and read only the important ones.
The first version is configurable and only reads senders address and subject.
In the next step I will try to summarize the e-mail body section by using AI tools like Ollama to summarize and than read aloud.

The script is already working, but got only few filters:
- download e-mails beetween two dates : DATE_SINCE, DATE_BEFORE
- filter and display only e-mails from senders mentioned in SENDER_DOMAINS
- filter and display also e-mails with chosen keywords KEYWORDS

  Requirements:
  - Python
  - pip install requests pyttsx3 beautifulsoup4

Just install requirements, run python nameofthescript.py and enjoy ;)
