# OSA-SBC

install brew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

- Run these two commands in your terminal to add Homebrew to your PATH:
    (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/ekaterina/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"

brew install flyctl
flyctl auth login
fly launch 
fly deploy

delete from fly.toml (
console_command = "/code/manage.py shell"
[deploy]
  release_command = "python manage.py migrate"
)






USer: testuser@gmail.com
Pass: Andrii123


123@gmail.com   Qwerty123zasdfg  Andrii