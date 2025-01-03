# InstaNinja
**InstaNinja** is a versatile Instagram automation tool that allows you to manage multiple accounts, interact with stories, follow/unfollow users, comment on posts, and scrape followers' data with ease.

![Screenshot 2024-09-19 110849](https://github.com/user-attachments/assets/e06b60ab-bc26-44b1-b140-56c572011a26)

## Features

- **Multi-account Management**
- **Story Viewing & Liking**
- **Follow & Unfollow**
- **Automated Commenting**
- **Followers Scraping**

## Requirements

- Python 3.6+
- `tkinter`
- `instagrapi`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ferid333/InstaNinja.git
   cd InstaNinja
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your configuration:**
   Run the `setup` command using the provided `Makefile` to create your `config.json` file:
   ```bash
   make setup
   ```
   Enter your Instagram username and password when prompted.

   **Alternatively**, you can manually edit the `config.json` file to add or modify **account credentials**:
   ```json
   {
     "accounts": [
       {
         "username": "your_username (required)",
         "password": "your_password (required)",
         "proxy": "your_proxy_address (optional)" 
       }
     ]
   }
   ```

## Usage

1. **Run the bot:**
   ```bash
   python3 bot.py
   ```
   or
   ```bash
   python bot.py
   ```

2. **Select an action:**
   Choose the **action** you want to perform (Send Message, Like Story, Follow, etc.).

3. **Enter required information:**
   Fill in the relevant fields (e.g., usernames, messages, post URLs).

4. **Perform the action:**
   Click on "Perform Action" to execute the selected task.

## How It Works

- **Account Switching:** InstaNinja automatically switches between accounts if multiple are configured.
- **Error Handling:** If an action fails, the bot will display an error message and move to the next account or action.
- **Processing Overlay:** While an action is in progress, a processing overlay will appear to indicate that the bot is working.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this project, make improvements, and submit pull requests!

## Note

Please do not use this bot for **spamming** or any other **harmful activities**.
