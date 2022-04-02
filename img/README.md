# What is this folder for? 🤔
If you would like to make your own [Discord Application](https://discord.com/developers/applications) to add any game of your liking, you can use the images I use.

## How would I make my own application? 👷‍♂️
Simple! Just go to the [Discord Application](https://discord.com/developers/applications) page and create a new application on the top right. After you picked a name (such as `Nintendo Switch`) you can change the name and multiple other settings! I use `Nintendo Switch` since that shows up when you start the app on Discord.

What you need to look for on the `General Information` page is the Application ID. This is what you'll use to connect to your application. *Note: To my current knowledge their is nothing wrong with having the ID known to the public, which as why I publicly published it on this GitHub page.*

After you have taken that ID you can hard code it into your application where you start the application. The code you change is below:

```python
RPC = Presence('YOUR ID HERE')
```

Once you've done that you can go to the `Rich Presence` tab and add the images you want to your application (make sure you follow the image guidelines!)

Lastly you want to create your own `games.json` file if you want to have an auto-updating game list. I host mine off of GitHub since it's free and easy to host it here. If you want to create your own `games.json` file to host off of GitHub you can just fork this project and change the `games.json` on your fork!
After you have created and updated your own `games.json` file you will need to update the code to use this new game list. The code you want to change is below:
```python
gamejson = requests.get('URL LINK HERE')
```

That's all you have to change to be able to use your own game list and still have the app auto-update on its own! But of course if you want a game added you can just ask instead of using your own game list ;)

# Copyright notice ⚠
I do not own **ANY** of these images, I just use them for my non-commercial application! Just a warning that you cannot use these images for commercial reasons or anything like that! You have been warned!
