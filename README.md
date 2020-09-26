# 📰 smart-RSS

RSS feed aggregator written in **python** with a little analytical twist. 

## Current features:

- Aggregate feeds from multiple sources
- Pre-process feeds by specifying stopwords in titles
- Plot basic text-analytics from the articles summary, titles and sources
- Customize look and settings via .toml
- Runs as a web-app (flask)

## How to use 
- Install dependecies
```python
pip install -r requirements.txt
```
- Customize config.toml
- Run app.py

# How to compile
```python
pyinstaller -noconsole -onefile -n smart-RSS ./app.py
```

## Planned features
- Expand the analytics (insights) from  data with more functions/graphs
- Dump data to a db for further analysis
- Compile it as a standalone app and provide binaries for win/linux
- Enhance ux/ui


## Screenshot
![screen1](https://github.com/raphael2692/smart-RSS/tree/master/screen/screen1.png?raw=true)
![screen2](https://github.com/raphael2692/smart-RSS/tree/master/screen/screen2.png?raw=true)
![screen3](https://github.com/raphael2692/smart-RSS/tree/master/screen/screen3.png?raw=true)
![screen4](https://github.com/raphael2692/smart-RSS/tree/master/screen/screen4.png?raw=true)
