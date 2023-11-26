# Lab-4 chat-bot
## Names, Majors, and Years
Luke Rowe, CSC, Grad Student

Jeremiah Lee, CSC, 5th-Year

Brandon Kwe, CSC, Grad Student

Yaniv Sagy, CSC, 4th-Year

## pog-bot description and mechanics
TODO:

## Phase 1
To accomplish phase 1 we started with the supplied code Dr. Foaad Gave us. With this code we modified the man loop to become a less nested, more filtered system. To accomplish this we made a helper function method named, `response_filter`. Response filter not only filters for responses that we wish to see the contents of, but also breaks up the response into four individual `sender, m_type, m_tar, msg`. The filter looks for messages that only the bot can read, it effectively whitelists only responses that are:
1. The `m_type` (message type) is `PRIVMSG`.
2. The `target` is the indicated channel the bot is in.
3. The `msg` starts with the botnames name with a : following right after

After the message is fully processed the following statements need only be if and elif statements asking what the `msg` contents are. Speficially for phase 1 we created all of the relevant "commands" for the bot which were all easy to implement with simple responses, however the user listing command was a little different. We created a brief helper function which will return the response of the bot issues a command to the channel asking for a list of `NAMES` formatting it and then returning it for the bot to send. This portion of the project was refined heavily and while it is very few lines, it was well thought out for the future of the project, Luke primarily laid the foundation for the start of this bot.

## Phase 2
To accomplish phase 2 we went off of phase 1's format and created a bot that responds to well stuctured predefined greeting terms. It can both prompt users and be prompted by users to say hello to them and see how they are doing. There is an internal timer that the bot runs on, that takes approximately 15 seconds for it to get annoyed/ try to progress the conversation. This timer was accomplished by making the recv on the socket timeout and return a dummy response containing the message dev-pass which we ignored. On timeout the code would run the timer checks and then go back to waiting.While this has the potential to miss inputs, we have yet to see such a thing as it executes the timer checks extremely quickly. It was also a lot more computationally and code efficient that making mutliple threads and locked variables.

The bot has a state system that it goes through, using the flowchart provided to us. It checks the current state and current message and if they match up then it flips through a list of predefined responses we made and chooses them relative to which part of the flowchart it is in.

## Individual Reports
### Luke Rowe
TODO:
### Jerimiah Lee
TODO:
### Brandon Kwe
TODO:
### Yaniv Safy
TODO:

