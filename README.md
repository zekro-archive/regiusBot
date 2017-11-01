# "KnechtBot" - Project name "regiusBot"

<img src="http://2.bp.blogspot.com/-Z6ktIvA-CuA/TnsTL9Irk9I/AAAAAAAAAME/svk5FJ43e-c/s1600/rip.jpg" width="200">

This project is dead. Because of various senseless bugs and crashed occured in last time which could not be comprehended in any way, I've decided to completely re-create this bot in Node.js. This project, named **Knecht V2**, can be found [**here**](https://github.com/zekroTJA/KnechtBot2).

---

## FAQ

### Is this a public bot and can I add it to my server?
No, this bot is hard coded for the ["Dark Devs" Development Discord server](http://discord.zekro.de) and will not work fully on other guilds. So no, this is not a public bot and you can not add it to your server. Also downloading and running the source will cause errors because the bot is set to my guilds ID.

### Why Python?
Because this bot is only running on one guild, so the performance of Python is sufficient for the system. Also I wanted to learn Python and so I had a project for that. And Python is a language wich is very easy to use and personally for me, it's kind of more fun creating bot functions in Python.

### Can I use your code for my project(s)?
Because I get a lot of questions about that, I've created a special **[policy](http://s.zekro.de/codepolicy)** for the usage of my code.

### What functions does the bot have?

#### Automatic Server Management
- **New Member Registration**<br>
When a user joins the server, the bot sends you a welcome message with a lot of information. You'll see also all online supporters and bots and user bots. Also the bot assigns you automatically the `@Devs` role on the server.<br><br>
![](https://image.prntscr.com/image/qkyBC7FMRoyVhihKZ_ZaHg.png)

- **User Bots System**<br>
With the `!invite <bot ID>` command, you can add your discord bot on the server. Then, when a supporter or admin adds the bot to the guild, the bot gets the role `@userbots` and will be renamed with bot owners name to show wich bot belongs to wich user.<br><br>
![](https://image.prntscr.com/image/HypIvJSBRbuuBFZ-8wzE4w.png)

- **Level System**<br>
Depending on your activity on the discord guild, you will get "Experience", wich will count up to a guild level. The top 20 is displayed in a scoreboard channel. *This system is still in beta and does not show the real activity value of the discord server members.*

- **Guild Members Statistic**
Every 10 minutes the bot collects the number of online members and registered users on the server and writes it into a google docs sheet. The statistic can be visited by entering the command `!stats`, wich shows a [link to the sheet](s.zekro.de/dcstats)<br><br>
![](https://image.prntscr.com/image/tZgRIuUOSXm0StaLrZnErg.png)<br>
*The displayed stats on the screenshsot are not up-to-date.*

#### User and Profiling Commands

- **`!github` Command**<br>
A command to link GitHub profiles to users and display them into a list. Also the linked github profile will  be shown in the user profile.<br><br>
![](https://image.prntscr.com/image/DFuvO_UVS7iCTlYbu37IaA.png)

- **`!dev` Command**<br>
A command wich adds (coding) language roles to users to display wich languages you can use and to mention those people in this roles to address your message to them.

- **`!prefix` Command**<br>
A command to register bot prefixes in a list to avoid multiple assignments of prefixes.<br><br>
![](https://image.prntscr.com/image/2fweIogOTuCdHDFWCKLXJA.png)

- **`!user` Command**<br>
A command wich displays the user profile of a server member with account information, bots on the guild the user is owner from, users level and the users GitHub account.<br><br>
![](https://image.prntscr.com/image/3JR38aFHT__sh_AOYr9xnA.png)

#### Other Functions

There are way more functions wich are not listed here. You can see them entering the `!help` command on my guild.<br><br>
![](https://image.prntscr.com/image/JL64h8wQRiWzWFtshewBaw.png)

---

## Used 3rd Party Packages

- [discord.py](https://github.com/Rapptz/discord.py)
- [request](https://pypi.python.org/pypi/requests)
- [BeautifulSoup](https://github.com/waylan/beautifulsoup)
- [gspread](https://github.com/burnash/gspread)
- [python-twitter](https://github.com/bear/python-twitter)
