from flask import jsonify
import json
payload_test ={
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

class Powerplant:
    def __init__(self,name,type,efficiency,pmin,pmax,wind=0,co2=0,load=0):
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax
        self.load = load
        self.wind = wind
        if self.type == 'windturbine':
            self.pmax = self.pmax * (self.wind /100)
    def calculate_co2_generated(self):
        self.co2 = self.load * 0.3
    def return_power(self):
        return {'name':self.name, 'p':self.load}

def calc_load_balancing(payload: dict):
    payload = json.loads(payload)
    lst_load = []
    pps =[]
    pp_pmins = []
    powerplants = sorted(payload['powerplants'], key = lambda i: i['efficiency'],reverse=True)
    for pp_types in powerplants:
        pps.append(pp_types['type'])
    pps = set(pps)
    wind = payload['fuels']['wind(%)']
    load = payload['load']
    price_kerosene = payload['fuels']['gas(euro/MWh)']
    price_gas =  payload['fuels']['kerosine(euro/MWh)']
    co2_price =  payload['fuels']['co2(euro/ton)']
    total_capacity = 0
    remaining_load = load
    KeyValList =[]
    powerplants_sorted =[]    
    if 'windturbine' in pps:
        KeyValList.append('windturbine')
        powerplants_sorted += [d for d in powerplants if d['type'] in KeyValList]
    if price_kerosene > price_gas:
        if 'turbojet' in pps:
            KeyValList =['turbojet']
            kerosene_plants = [d for d in powerplants if d['type'] in KeyValList]
            powerplants_sorted += kerosene_plants
        if 'gasfired' in pps:
            KeyValList =['gasfired']
            gas_plants = [d for d in powerplants if d['type'] in KeyValList]
            powerplants_sorted += gas_plants
    elif price_kerosene < price_gas:
        if 'gasfired' in pps:
            KeyValList =['gasfired']
            gas_plants = [d for d in powerplants if d['type'] in KeyValList]
            powerplants_sorted += gas_plants
        if 'turbojet' in pps:
            KeyValList =['turbojet']
            kerosene_plants = [d for d in powerplants if d['type'] in KeyValList]
            powerplants_sorted += kerosene_plants
    for idx,pp in enumerate(powerplants_sorted):
        if remaining_load > 0:
            if pp['type'] != 'windturbine':
                plant = Powerplant(name=pp['name'],
                               type=pp['type'],
                               efficiency=pp['efficiency'],
                               pmin=pp['pmin'],
                               pmax=pp['pmax'],
                               )
            elif pp['type'] == 'windturbine':
                plant = Powerplant(name=pp['name'],
                               type=pp['type'],
                               efficiency=pp['efficiency'],
                               pmin=pp['pmin'],
                               pmax=pp['pmax'],
                               wind=wind
                               )
            total_capacity +=  plant.pmax
            
            for pmin in powerplants_sorted:
                pp_pmins.append(pmin['pmin'])
            
            if remaining_load >= plant.pmax and remaining_load > plant.pmin:
               
                if remaining_load - plant.pmax < pp_pmins[idx+1]:
                    dif = pp_pmins[idx+1] - (remaining_load - plant.pmax)
                    plant.load = round(plant.pmax) - dif
                    remaining_load -= plant.load
                else:
                    plant.load = round(plant.pmax)
                    remaining_load -= plant.load
                    
            elif remaining_load < plant.pmax and remaining_load >= plant.pmin:
                plant.load = round(remaining_load)
                remaining_load -= plant.load
            if remaining_load < plant.pmin & remaining_load > 0:
                return ValueError('Load is lower than min capacity required!')
            lst_load.append(plant.return_power())

    if load> total_capacity:
        return ValueError('Load is higher than capacity!')
    return jsonify(lst_load)


## for testing purposes
if __name__ == '__main__':


  print(calc_load_balancing(payload_test))