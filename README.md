# ~Enhanced Maunium sticker picker
Bring your custom stickers into Element nicely.

https://github.com/user-attachments/assets/c8dbf68f-46b8-4996-87eb-103daf093da2
## What this fork brings
This is based on [xz-dev's fork](https://github.com/xz-dev/stickerpicker) of the original [Maunium sticker picker](https://github.com/maunium/stickerpicker).

Over [xz-dev](https://github.com/xz-dev/)'s fork, this contains the following changes:
- Animated thumbnails of stickers
- Makes **mass-importing** of stickers easy with a script (hundreds or more)
- Includes a script for **mass-setting the dimensions** of all stickers, or selected ones
- There is a script which converts all JPGs/JPEGs to PNGs
- **Disables Giphy search, as I don't use it for my instance** (the button is hidden)
	- though, below you can find a quick guide on setting up giphyproxy and enabling support, in case you want it.

Over the original Maunium sticker picker, xz-dev's fork brings the these noteworthy improvements:
- Animated sticker support
- Improved webp performance
- Added webm support (animated)
- Added webm transparency
- ... more stuff - see commits [here](https://github.com/maunium/stickerpicker/compare/master...xz-dev:stickerpicker:master)
## Setup overview

If you prefer a video, [Brodie Robertson](https://www.youtube.com/c/BrodieRobertson) has made [a great video](https://youtu.be/Yz3H6KJTEI0) on setting up the picker and creating some packs. This is a bit old, and made for the original sticker picker, but will still work.

Setting this up is pretty easy. What you need:
- A place to host your stickers. Can be [Github Pages](https://github.com/maunium/stickerpicker/wiki/Hosting-on-GitHub-pages), or your own webserver
	- *the guide below assumes you want to host them on your own server. if you plan on using Github Pages, you can skip the big Webserver setup section, and jump to Step 7.*
- Stickers. You can get some [here](https://discords.com/emoji-list) or [here](https://emoji.gg/) if you don't have any
- Python
## Instructions
##### Webserver setup
1. `git clone https://github.com/shootie22/matrix-stickerpicker.git`
2. `cd` in and set up a virtual environment:
	1. Create with `virtualenv -p python3 .venv`
	2. Activate with `source .venv/bin/activate`
3. Install the utility commands and their dependencies with `pip install .`
4. Make a folder and place your stickers inside
5. Run `python process_stickers.py` and follow the instructions.
###### Optional: use tools (resize, convert, rename)
You may want to use some of these tools to create a better sticker picking experience.
- `python resize.py` - resizes all stickers to a specified size. follow prompts
- `python jpgtopng.py` - convert jpgs to pngs. the importer doesn't like some jpgs
- `python rename.py` - I didn't want any numbers, prefixes or suffixes for my sticker names. use this if you don't want them either.
##### Serving the picker through Nginx/Apache
6. Example Nginx config:
```
server {
	listen 80;
	server_name stickers.your.tld;

	// WARNING: careful here, only serve the web folder, NOT the whole git repo.
	// otherwise you will also be serving your config.json which
	// contains your account's access token.
	root /var/www/stickers/web;
	index index.html;

	location / {
		try_files $uri $uri/ =404;
	}
}
```
6. Example Apache config:
```
<VirtualHost *:80>
    ServerAdmin admin@your.tld
    ServerName stickers.your.tld

	// WARNING: careful here, only serve the web folder, NOT the whole git repo.
	// otherwise you will also be serving your config.json which
	// contains your account's access token.
    DocumentRoot /var/www/stickers/web

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    <Directory /var/www/stickers/web>
        Require all granted
    </Directory>
</VirtualHost>
```
*run your config through certbot afterwards to get an SSL cert*
##### Getting the stickers onto Element
7. In chat, type `/devtools`
8. Click on Explore account data
9. Look for `m.widgets`
	9. If it doesn't exist, click on Send custom account data event and use `m.widgets` as the event type
10. Paste this in the Event Content box, after editing it to match your details:
```json
{
  "stickerpicker": {
    "content": {
      "type": "m.stickerpicker",
      "url": "https://stickers.your.tld/?theme=$theme",
      "name": "Stickerpicker",
      "creatorUserId": "@user:your.tld",
      "data": {}
    },
    "sender": "@user:your.tld",
    "state_key": "stickerpicker",
    "type": "m.widget",
    "id": "stickerpicker"
  }
}
```
*fields you need to change: url, creatorUserId, sender.*

Final step: restart Element.

If you did it correctly, you should see the stickers appear in your Stickers panel.

For other people to use the sticker picker, all they have to do is paste your edited config into their `m.widgets`. 
## Giphyproxy
This is optional, only needed if you want to use the gif picker.

Giphyproxy is a Matrix media server, essentially a stripped down Matrix server which only deals with media.

⚠️Heads-up: this does not seem to work on a closed-federation Matrix server, which is also why I'm not using it. if your server has an open federation, it will probably work.

Two things are needed to make the gif picker work: enabling the button, and hosting your Giphyproxy instance.
##### Hosting your Giphyproxy instance under docker
1. `cd giphyproxy` and build the docker image using
	`docker build -t giphyproxy .`
2. Once it's built, you need to generate a server_key using
	`docker run --rm giphyproxy giphyproxy -generate-key`
3. Place the key it gave you into the config. Also, rename the config to `config.yaml`
4. Populate the other fields like `server_name` or `port` if you want to run it on a port other than boob.
	`server_name` has to be something other than your Matrix server's name. Remember, it's a different server.
5. Start the container using
	`docker run -d --name giphyproxy -p 8008:8008 -v $(pwd)/config.yaml:/data/config.yaml:ro giphyproxy`
6. Check if it's running using `docker ps -a`. If you see it running, you're good to go.

You can check logs using `docker logs giphyproxy` to debug it if it doesn't work.
Once it works, it won't output anything and will simply keep running.
##### Enabling the gif button in the picker
1. Go to `web/src/giphy.js`
2. Give it your own API key (or leech off of Maunium's). You can generate one [here](https://developers.giphy.com/dashboard/)
3. Set the `GIPHY_MXC_PREFIX` of your server. It should be exactly what you set in Giphypicker's `server_name` field, prefixed by `mxc://`
4. On line 9, in the giphyIsEnabled() function, remove `return false` and uncomment `//return GIPHY_API_KEY !== "" `:
```js
export function giphyIsEnabled() {
	return false
	//return GIPHY_API_KEY !== ""
}
```

That's pretty much it. Whenever you change something in the web parts, you'll have to restart Element. So do that, and you should see the gif button, with the gif search working. Hopefully.
##### Bonus Giphysearch digging
I couldn't find any documentation on it, but luckily the program is small and easy to understand by reading the code. It all lives in main.go.

What it does is it serves the gif content you send as a sticker, through the Matrix media protocol `mxc://`. This is because when you send a gif, it's still sent as a sticker, which can only have an `mxc://` as its source; it cannot be a direct image resource. Because of this, Giphyproxy needs to serve images through that.

And because this is basically a separate server, you will have to federate with it in order to display the gifs you send, otherwise they will be empty. By checking the console, I found out my server was rejecting the requests and saying "Refusing to federate with gifs.my.tld", as I'm running a closed federation setup. Even then, it shouldn't be doing that, as I added by source to my federation whitelist. Maybe I did something wrong, maybe it just doesn't work.

I did all of this in a pretty "let's see if I can get it to work" manner on a Saturday, so it may not be state-of-the-art, but it works. Hope you were able to get it to work too. It was worth it.

I left some stickers in there for those reading this whole readme until the end. Just for you.

Feel free to open issues or contribute if you feel like it.
