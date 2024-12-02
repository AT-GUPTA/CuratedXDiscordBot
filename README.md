### [GPT generated readme]
---
# CuratedX Discord Bot

CuratedX is a customizable Discord bot designed to streamline link sharing and curation within a server. It detects links posted in a designated channel, allows members to upvote them, and curates the most popular links in a separate channel. With rich embed formatting, dynamic configurations, and an easy-to-use command interface, CuratedX is perfect for maintaining a high-quality content feed in any community.

---

## **Features**

- **Link Detection**: Automatically detects links in a designated `#links_only` channel.
- **Reaction-Based Curation**: Members can upvote links using a reaction emoji, and links meeting the required upvote threshold are posted in a curated channel.
- **Embed-Based Curated Posts**: Links are posted as clean, formatted embeds in the curated channel.
- **Dynamic Configuration**: Administrators can change the upvote threshold and reaction emoji without restarting the bot.
- **Command Interface**:
  - View bot stats.
  - Reset tracked messages.
  - Update settings dynamically.
  - Help command for quick guidance.
- **Error Handling**: Provides meaningful feedback for command misuse and logs key events for easier debugging.

---

## **Setup Instructions**

### **1. Prerequisites**
- Python 3.9 or higher
- A Discord Developer account (to create and manage your bot)
- Basic understanding of Python and Discord bot permissions

---

### **2. Creating the Bot**

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and add a bot to it under the **Bot** section.
3. Copy the bot token for later use.
4. Enable the following intents under the **Privileged Gateway Intents** section:
   - Server Members Intent
   - Message Content Intent

---

### **3. Setting Up Locally**

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/CuratedXDiscordBot.git
   cd CuratedXDiscordBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following variables:
   ```
   BOT_TOKEN=your_bot_token_here
   LINKS_ONLY_CHANNEL_ID=your_links_only_channel_id
   CURATED_CHANNEL_ID=your_curated_channel_id
   USER_COUNT=2
   REACTION_EMOJI=👍
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

---

### **4. Adding the Bot to Your Server**

1. Generate an invite link:
   - Go to the **OAuth2 > URL Generator** section in the Discord Developer Portal.
   - Select the following scopes: `bot`.
   - Under **Bot Permissions**, select:
     - Read Messages/View Channels
     - Add Reactions
     - Send Messages
     - Manage Messages (optional, for deleting non-link messages)
   - Copy the generated invite link and paste it into your browser to invite the bot to your server.

2. Ensure the bot has the necessary permissions in the `#links_only` and `#curated` channels.

---

## **Commands**

| Command               | Description                                                                                     | Admin Only |
|-----------------------|-------------------------------------------------------------------------------------------------|------------|
| `!stats`              | Shows the number of messages currently being tracked for reactions.                            | No         |
| `!reset`              | Resets all tracked messages.                                                                   | Yes        |
| `!set_user_count <n>` | Updates the number of reactions required to curate a link.                                      | Yes        |
| `!set_reaction <emoji>`| Updates the reaction emoji used for upvotes.                                                   | Yes        |
| `!help`               | Displays a list of available commands with descriptions.                                        | No         |

---

## **How It Works**

1. Post links in the designated `#links_only` channel.
2. React to links with the configured reaction emoji (default: 👍).
3. When a link reaches the required number of upvotes (default: 2), the bot curates it by posting it in the `#curated` channel.
4. Non-link messages in the `#links_only` channel are automatically deleted.

---

## **Customization**

The bot is designed to be easily customizable. You can:
- Change the reaction emoji via the `!set_reaction` command or by updating the `.env` file.
- Adjust the upvote threshold using the `!set_user_count` command or `.env` file.
- Modify the embed format for curated posts to better match your server’s theme.

---

## **Error Handling**

- The bot logs key actions, such as link detection and reactions, for easier debugging.
- Users are informed if they attempt to execute commands without proper permissions or arguments.

---

## **Deployment**

To keep the bot running 24/7, you can deploy it on a cloud platform. Popular options include:
- [Daki](https://daki.cc/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Heroku](https://heroku.com/) (free tier may have limitations)
- [Replit](https://replit.com/)

---

## **Contribution**

Feel free to fork this repository and submit pull requests for any enhancements.

---

## **License**

This project is licensed under the MIT License. You are free to use, modify, and distribute it as long as you include the original license.

---

Let me know if any adjustments are needed! 🚀
