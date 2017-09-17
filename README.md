# Bittrex-Notify GUI

GUI for sorting/filtering/notification of coins which are increasing in price. Can be used as an aid in locating short term investments. Written in/for Python 3+

![Bittrex-NotifyGUI](https://github.com/JevinJ/Bittrex-Notify/blob/master/BittrexNotifyGUI.jpg?raw=true)
### Prerequisites

Python 3+

Libraries:
```
playsound
urllib3
certifi
```

Optional:
```
always-on-top(uses Autohotkey) or other program that will keep windows on top.
```

### Installing

Install playsound Via pip3
```
In terminal/command prompt type:
pip3 install playsound
```

Install urllib3 Via pip3
```
In terminal/command prompt type:
pip3 install urllib3
```

Install certifi Via pip3
```
In terminal/command prompt type:
pip3 install certifi
```

Optional:
```
Unzip and run always-on-top downloaded from [here](https://www.labnol.org/software/tutorials/keep-window-always-on-top/5213/)]
Once Bittrex-Notify and always-on-top are running press Ctrl+Space with the Bittrex-Notify window selected to keep it on top.
```

### Running

Download or clone the repository.
In the download location make sure you have in the /src/ folder:

Folders:
```
fast_history
media
slow_history
```

Python files:
```
fasttick.py
main.py
slowtick.py
```
Open a terminal/command prompt in the /src/ folder and type:

Terminal:
```
python3 main.py
```

Command Prompt:
```
python main.py
```

### Usage

```
On first run for all listboxes, if there is any new data it will be updated to the box after the second cycle.
Both windows will only show coins with volumes >= 350 BTC
The first window cycles every 10 minutes and shows changes >= 3% and coins with price >= .00001000.
The second window cycles every 15 seconds and shows average rate >= .2%.
You can press the bell button to play a sound when the box updates, if it has any data to update on.
This program will not give 100% accurate reccomendations or certainty that the price will continue to increase. You should use your own judgement and research on Bittrex to choose which coins to invest in or avoid.
```

## Authors

* **Jevin Jones** - *Creator* - [JevinJ](https://github.com/JevinJ)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
