# powerplant-coding-challenge-solution


## Welcome !

Below you can find guide to running this solution.


## .requirements

* python3 

* flask



## .installation
pip install -r requirements.txt

## .running locally
starting server:

```
python app.py
```

## .running in Docker

```docker build -t flask-app:latest .  ```


```docker run -it --rm -p 8888:8888 flask-app```

Once the container finished loading and is all started up, you'll be informed that the flask server is up and running.


Send POST request to http://127.0.0.1:8888/calculate

with body:

```
{
  "load": 480,
  "fuels":
  {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredbig2",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredsomewhatsmaller",
      "type": "gasfired",
      "efficiency": 0.37,
      "pmin": 40,
      "pmax": 210
    },
    {
      "name": "tj1",
      "type": "turbojet",
      "efficiency": 0.3,
      "pmin": 0,
      "pmax": 16
    },
    {
      "name": "windpark1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    },
    {
      "name": "windpark2",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 36
    }
  ]
}
```

The response will be:

```[
  {
    "name": "windpark1",
    "p": 90
  },
  {
    "name": "windpark2",
    "p": 22
  },
  {
    "name": "gasfiredbig1",
    "p": 368
  }
]
```


.The merit order is based on the efficiency and price per MWh, obviously the wind turbines are always the first priority given the facts.



.TODO will add co2 cost if time allows.
