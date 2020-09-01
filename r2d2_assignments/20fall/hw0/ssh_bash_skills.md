## SSH to Control Raspberry Pi
### 1. Build the Raspberry Pi Systems
The [Raspberry Pi Zero](https://en.wikipedia.org/wiki/Raspberry_Pi#Pi_Zero) uses a [micro SD card](https://en.wikipedia.org/wiki/SD_card#Micro) as the storage space, so we could install the operating system by writing the image file to the micro-SD card. We should have done this step for you, but you could still rebuild the whole system by following the steps below:

* Download the [image file](https://drive.google.com/file/d/1XCulQIJeKBYETBc-63kWurN-2qw5MeHO/view?usp=sharing) from the google drive.
* Connect a [USB SD card reader](https://www.amazon.com/s?k=micro+sd+card+reader) with the SD card inside to your computer.
* Flash the image to the SD card, here we recommend a free software [balenaEtcher](https://www.balena.io/etcher/) which is available for all platforms.

### 2. Connect the Raspberry Pi to Wi-Fi
After the SD card is flashed, you need to set up the Wi-Fi. Download this [configuration file](wpa_supplicant.conf) (keep the filename as `wpa_supplicant.conf`) which contains the following details:

```shell
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
  ssid="WIFI_NETWORK_NAME"
  psk="WIFI_PASSWORD"
}
```

You need to insert the your Wi-Fi name `WIFI_NETWORK_NAME` and password `WIFI_PASSWORD` and then put this file in the `boot` partition of the SD card. If you are using Windows and the prompt comes up saying you should format the disk before using it, **DO NOT** format it. Just look for the partition with name `boot`.

Then eject the SD card safely and plug it back to the slot on the Raspberry Pi and turn it on. If everything goes well, the Raspberry Pi is connected to your Wi-Fi now.

For student that doesn't have a private Wi-Fi network, you can use the Wi-Fi Hotspot feature on your computer or mobile devices. Or if you're on campus, you can use `AirPennNet-Device` by following the instructions [here](https://www.isc.upenn.edu/how-to/using-wireless-penn#For-devices). The MAC address of your Raspberry Pi should be listed on the device body.

#### Connect to Raspberry Pi via USB Serial

For students that don't have a SD card reader and wants to start immediately, you can try out the more advanced method to temporarily connect to your RPi via USB serial. Simply plug a micro USB cable from the USB OTG port on the RPi to your computer, and there should be a new serial TTY/COM device pops up. Connect using PuTTY on Windows or `screen` command line tool on Linux/MacOS. You can look for more information online.

### 3. SSH into Raspberry Pi
Before using SSH, we must first know the IP address of the Raspberry Pi. We could use the IP scanner apps to find the IP address, here are some free software:


| Android/iOS |  MacOS  |       Windows       | Linux/Windows/MacOS |
|:-----------:|:-------:|:-------------------:|:-------------------:|
|     [Fing](https://www.fing.com/products)    | [Lanscan](https://apps.apple.com/us/app/lanscan/id472226235?mt=12) | [Advanced IP Scanner](https://www.advanced-ip-scanner.com/index2.php) |   [Angry IP Scanner](https://angryip.org/download/#linux)  |

<table><tr>
<td> <img src="images/Fing.png" alt="Drawing" style="width:150px;" /> </td>
<td> <img src="images/Lanscan.png" alt="Drawing" style="width: 600px;"/> </td>
</tr>
</table>

After you find the IP address of the Raspberry Pi, it's time to SSH into it. The default username to login to the Raspberry Pi is **`pi`** and the password is **`raspberry`**. There are many tutorials online for how to use SSH, here, we'll just give some simple instructions on different platforms.

* **Windows**
	* Using Windows 10's built-in SSH commands, click [here](https://www.howtogeek.com/336775/how-to-enable-and-use-windows-10s-built-in-ssh-commands/) for details. Once SSH client is installed, you can follow the same steps below for MacOS / Linux.
	* Another option is [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), download and install it. PuTTY has a GUI where you can insert in the IP address and it will launch a terminal window. Then you just need to type the username (`pi`) and password (`raspberry`) and you are good to go.

<table><tr>
<td> <img src="images/putty1.jpg" alt="Drawing" style="width:300px;" /> </td>
<td> <img src="images/putty2.jpg" alt="Drawing" style="width: 500px;"/> </td>
</tr>
</table>

* **MacOS / Linux**

Open a terminal window and then run:

```shell
ssh pi@xxx.xxx.xxx.xxx
[enter the password when prompt]
```

Where `xxx.xxx.xxx.xxx` is the IP address of your Raspberry Pi.

### 4. Basic Bash Skills

Many tutorials on bash commands available online, here we just introduce some useful commands which are frequently utilized.

* `cd` **Change Directory:** `cd folder` to change to the working directory you are currently under to `folder`, see more details [here](https://linuxize.com/post/linux-cd-command/).

* `ls` **List Files/Directory:** `ls folder` to list information about files and directories under `folder`, see more details [here](https://linuxize.com/post/how-to-list-files-in-linux-using-the-ls-command/).

* `cat` **Display/Copy/Create Text Files:** `cat filename` to display the content of a file with `filename`, see more details [here](https://www.interserver.net/tips/kb/linux-cat-command-usage-examples/).

* `rm` **Remove File/Directory:** `rm filename` to remove a file or directory with `filename`, see more details [here](https://www.computerhope.com/unix/urm.htm).

* `nano` **Text Editor:** `nano filename` to edit the file with `filename`. It's a command-line based text editor, see more details [here](https://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/).

* `password` **Change the password:** It is recommended to change the password once you get your Raspberry Pi.

* `screen` **Start a terminal session in the background:** `screen -S name` to start a named session called `name`. Press `Ctrl-A` and then press `D` to detach the session.  `screen -r name` to attach to the session called `name`. This allows you to start a terminal that won't be terminated when you disconnect from SSH. See more details [here](https://linuxize.com/post/how-to-use-linux-screen/).

* **Commands for Raspberry Pi:** 
	* System configuration: `sudo raspi-config`
	* Reboot: `sudo reboot now`
	* Shutdown: `sudo shutdown now`
	
	You should ***always*** shut down properly before you unplug the power. Failed to do so may result in data corruption, and you may need to re-flash the image when that happens.
