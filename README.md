Sure, here's an updated GitHub README for Luna, a Discord bot written in Python, with information about the repository you provided:

---

# Luna - Discord Bot for ESTIN

Luna is a versatile Discord bot developed for the ESTIN (École Supérieure en Sciences et Technologies de l'Informatique et du Numérique) community. Built in Python, Luna provides a range of commands designed to enhance your Discord experience, from server management to interactive features.

## Table of Contents

- [Commands](#commands)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Commands

Here is a list of commands available in Luna:

- `!serverinfo`
  - Provides information about the server.
  
- `!help [command]`
  - Displays the help menu or information about a specific command.
  
- `!userinfo [member]`
  - Retrieves information about a specified member.
  
- `!roll [sides=6]`
  - Rolls a die with the specified number of sides (default is 6).
  
- `!poll <question>`
  - Creates a poll with the specified question.
  
- `!invite`
  - Provides an invite link for the bot.
  
- `!clear <amount>`
  - Clears a specified number of messages from the channel.
  
- `!ping`
  - Checks the bot's latency.
  
- `!capitaltrivia`
  - Starts a trivia game about world capitals.
  
- `!avatar [member]`
  - Displays the avatar of a specified member.
  
- `!sources`
  - Lists the sources or credits related to the bot.
  
- `!create_channel <channel_name>`
  - Creates a new channel with the specified name.
  
- `!delete_channel <channel_name>`
  - Deletes the specified channel.
  
- `!games <name>`
  - Launches a game or provides information about a game with the specified name.
  
- `!chat <msg>`
  - Sends a message to the chat.
  
- `!tts <text>`
  - Sends a message with text-to-speech enabled.
  
- `!join`
  - Makes the bot join the voice channel.
  
- `!among <time> <msg>`
  - Schedules a message to be sent in an "Among Us" style game.
  
- `!rating <name> <rating_type>`
  - Provides a rating for the specified name and type.
  
- `!g <message>`
  - Sends a message with text-to-speech enabled.
  
- `!leave`
  - Makes the bot leave the voice channel.
  
- `!addadmin <member>`
  - Grants admin privileges to the specified member.

## Installation

To set up Luna on your own server, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Untitled-Master/Luna-os.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd Luna-os
   ```

3. **Install Dependencies:**
   Ensure you have Python 3.8+ installed, then create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. **Configure the Bot:**
   Create a `.env` file based on the `.env.example` file and provide your Discord bot token and other necessary credentials.

5. **Run the Bot:**
   ```bash
   python bot.py
   ```

## Usage

Once Luna is set up and running, invite it to your Discord server using the invite link provided by the `!invite` command. You can then use the available commands to manage and interact with your server.

## Contributing

Contributions are welcome! If you would like to contribute to Luna, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Open a pull request with a detailed description of your changes.

## License

Luna is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any questions or support, please open an issue on the [GitHub repository](https://github.com/Untitled-Master/Luna-os) or reach out to the maintainers. Enjoy using Luna on your Discord server!

