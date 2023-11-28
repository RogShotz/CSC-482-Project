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
To accomplish phase 2 we went off of phase 1's format and created a bot that responds to well stuctured predefined greeting terms. It can both prompt users and be prompted by users to say hello to them and see how they are doing. There is an internal timer that the bot runs on, that takes approximately 15 seconds for it to get annoyed/try to progress the conversation. This timer was accomplished by making the recv on the socket timeout and return a dummy response containing the message dev-pass which we ignored. On timeout the code would run the timer checks and then go back to waiting. While this has the potential to miss inputs, we have yet to see such a thing as it executes the timer checks extremely quickly. It was also a lot more computationally and code efficient that making mutliple threads and locked variables.

The bot has a state system that it goes through, using the flowchart provided to us. It checks the current state and current message and if they match up then it flips through a list of predefined responses we made and chooses them relative to which part of the flowchart it is in.

## Individual Reports
### Luke Rowe
My contribution was having a q/a bot that answers any prompt with a `who` and `pres` in the message. It will then extract any number in the text and look for the president who corresponds with the number. From there I use BS4 to strip a wiki list of all components including `[pres_num, pres_name, pres_birth, pres_death, pres_term, pres_party, pres_election, pres_VP]`. With this data the bot extracts all info, including small little bonus things including in the wiki including `[c] == lack of political parties, [d], [g], [l] == diff party as P and VP, [e] == death in office, [f], [n] == new party, [h] = resigned, [j] == expelled from party, [t] = new VP`. This is displayed to the user in a bracketed text and was not further extrapolated due to the nature that I did not want to write 10+ if statements with new sentence parameters since I had already done that for about 5 hours total. I also implemented my own dictionary with the relative terms for first second, etc up to 99. I thought of a pretty clever NLP strategy to automate what each number correlates to.

In addition I added the function to query the bot with `tell me more about {pres name}` and any name even if shortened will respond with more info about presidents with that name, i.e. bill clinton for `bill`, or all the georges for `george`, etc.

In relation to our project I feel that navigating wiki, keying information, and reporting it all to a localized csv helps us a lot so that we can gather genelogical data easily. Additionally I went beyond the scope of the project to make sure that the bot cleans any data that we do not want, has local dev related messages it can parse through, and does not block on any given waited input to make sure that the bot progresses. I will admit a large part of the time I committed to this bot was spent on developing the bot. I have previous chat-bot experience as an employee making discord-bots so I wanted to make it up to the standards we had back then.
### Jerimiah Lee
TODO:
### Brandon Kwe
For Phase III, I gave our bot the ability to answer the question "When was *name* born?", *name* being the name of a famous person, historical figure, and some famous animals. This question works first by parsing the name of the person out from the IRC message. This name is then passed to the Wikipedia api call which returns the summary section of the Wikipedia article. I then use some string manipulation to strip the return string of everything but the date of birth. If the input message does not yield a valid date of birth either because the name is ambiguous or is not a person with a Wikipedia entry, the bot responds with a message indicating such: "I'm sorry, I'm not sure when *name* was born.".

Some sample names I tested with and know work:
"Xi Jinping", "Donald Trump", "Bill Burr", "Jesus Christ", "Julius Caesar", "RBG", "Mike Trout", "Winston Churchill", "Shakespeare", "Koko gorilla", "Phil Ivey"
### Yaniv Sagy
For Phase III, I created an NBA data feature where the bot can respond to questions such as "NBA: Which team did [NBA team] win against on [date]?" or "NBA: Who lost to [NBA team] on [date]?". I initially wrote a Python script that used BeautifulSoup to parse a variety of NBA game data from basketball-reference.com that spanned across multiple years. I collected data such as the home team and visiting team, the points they each scored, the stadium they played in, and the amount of fans in attendance, and wrote the data to a CSV file that has been saved as nba_data.csv.

To directly answer the questions pertaining to which NBA team beat or lost to other teams on any given date, I created a module named yaniv_bot that runs a function that initially reads in the CSV file and transforms it to a pandas DataFrame. Then, when a user asks a question of the form `NBA: Who [beat/won against/defeated/lost to/lost against/fell to] [NBA team] on [date]?`, `NBA: Who did [NBA team] [beat/win against/defeat/lose to/fall to] on [date]?`, `NBA: Who did [NBA team] play against on [date]?`, or `NBA: Who played against [NBA team] on [date]?`, spacy was used to execute a dependency graph parse in order to determine the pronouns, subjects, objects, and numbers (date of the form `MM/DD/YYYY` or `MM/YYYY` or `YYYY`) in the input message. From these parts of speech and dependency relations, intuition could be built as to whether or not the noun in the input message was the subject performing the verb or the object being affected by the verb. With this knowledge, the data could be used to filter out the relevant NBA game and date rows from the pandas DataFrame, in addition to counting the number of times the team in question has won or lost games on the specified date. This data is then returned as a list of NBA game results back to the user that made the query to the bot.

