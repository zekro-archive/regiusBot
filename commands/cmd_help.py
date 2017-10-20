from discord import Embed, Color

description = "Help"


CMDMAP = None


async def ex(message, client):
    await client.send_message(message.author, embed=Embed(
        color=Color.green(),
        title="knechtBot - Help",
        description="**[Here](https://docs.google.com/spreadsheets/d/e/2PACX-1vR_XkUXIhCNhnpqFu3N-grcDRWzLSTtZgtdRjdzMkhnS1n40_d9oITfEz1LzAKpDlLuTsmiiwUfbOh0/pubhtml)** you can see" \
                    "a full list of all user available commands of this bot! ;)"
    ).set_image(url="https://media.giphy.com/media/nY5qTLViCYjIc/giphy.gif"))
    await client.delete_message(message)