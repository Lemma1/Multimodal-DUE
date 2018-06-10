import os
import numpy as np
from collections import OrderedDict
import sys
sys.path.append("/home/lemma/Documents/MAC-POSTS/side_project/network_builder")
import MNMAPI
from MNM_mcnb import *

IMPLEMENT_TYPES = ['single_drive', 'multiple_drive', 'transit', 'pnr', 'metro']


UNIT_TIME = np.float(5)
T2M = np.float(0.1)


class parking_lot():
  def __init__(self, base_price):
    self.base_price = base_price

  def get_price(self):
    return self.base_price

  def get_cruise_time(self, t):
    return 0

# class link():
#   def __init__(self):
#     pass

#   def update_cc(self, in_cc, out_cc):
#     self.in_cc = in_cc
#     self.out_cc = out_cc

#   def get_tt(self, t):
#     return 0


class base_path(object):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, ID_list, O, D):
    self.target_time = target_time
    self.early_penalty = early_penalty
    self.late_penalty = late_penalty
    self.ID_list = ID_list
    self.O = O
    self.D = D
    self.path_type = path_type

  def get_cost():
    raise Exception('Method in base class should not be called!')

  def get_travel_time():
    raise Exception('Method in base class should not be called!')

  def get_wrongtime_penalty(self, arrival_time):
    return np.max(self.late_penalty * (arrival_time - self.target_time), self.early_penalty * (self.target_time -arrival_time))

class driving_route(base_path):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, O, D, ID_list, link_list, path_ID, number_people, parking_lot, walking_time1, walking_time2):
    assert(number_people >= 1)
    super(driving_route, self).__init__(path_type, target_time, early_penalty, late_penalty, ID_list, O, D)
    self.link_list = link_list
    self.path_ID = path_ID
    self.number_people = number_people
    self.parking_lot = parking_lot
    self.walking_time1 = walking_time1 / UNIT_TIME
    self.walking_time2 = walking_time2 / UNIT_TIME

  def get_travel_time(self, t, link_ID_list, dta):
    arrival_time = t + self.walking_time1
    for link_ID in self.link_list:
      idx = link_ID_list.index(link_ID)
      arrival_time += dta.get_car_link_tt(np.array[arrival_time])[idx, 0]
    arrival_time += self.walking_time2
    arrival_time += self.parking_lot.get_cruise_time(arrival_time)
    return arrival_time - t

  def get_carpool_cost(self):
    return self.number_people

  def get_amortized_parkingfee(self):
    return np.float(self.parking_fee) / np.float(number_people)


  def get_cost(self, t, link_ID_list, dta):
    tt = self.get_travel_time(t, link_ID_list, dta)
    late_penalty = self.get_wrongtime_penalty(t + tt)
    return T2M * tt + late_penalty + self.get_carpool_cost() + self.get_amortized_parkingfee()

class transit_route(base_path):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, O, D, ID_list, link_list, path_ID, transit_fare, walking_time1, walking_time2, transit_time):
    super(transit_route, self).__init__(path_type, target_time, early_penalty, late_penalty, ID_list, O, D)
    self.link_list = link_list
    self.path_ID = path_ID
    self.transit_fare = transit_fare
    self.walking_time1 = walking_time1 / UNIT_TIME
    self.walking_time2 = walking_time2 / UNIT_TIME
    self.transit_time = transit_time / UNIT_TIME

  def get_travel_time(self, t, link_ID_list, dta):
    arrival_time = t + self.walking_time1
    arrival_time += self.transit_time
    for link_ID in self.link_list:
      idx = link_ID_list.index(link_ID)
      arrival_time += dta.get_trcuk_link_tt(np.array[arrival_time])[idx, 0]
    arrival_time += self.walking_time2
    return arrival_time - t

  def get_transit_fee(self):
    return self.transit_fare

  def get_transit_inconvenience(self):
    return np.float(0)

  def get_cost(self, t, link_ID_list, dta):
    tt = self.get_travel_time(t, link_ID_list, dta)
    late_penalty = self.get_wrongtime_penalty(t + tt)
    return T2M * tt + late_penalty + self.get_transit_fee() + self.get_transit_inconvenience()

class park_ride_route(base_path):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, O, D, ID_list, car_link_list, car_path_ID, 
                        transit_link_list, transit_path_ID, parking_lot, transit_fare, 
                        before_drive_walking_time, switching_time, after_transit_walking_time, transit_time):
    super(park_ride_route, self).__init__(path_type, target_time, early_penalty, late_penalty, ID_list, O, D)
    self.driving_part = driving_route(path_type, target_time, early_penalty, late_penalty, O, D, ID_list, car_link_list, car_path_ID, 1, parking_lot, before_drive_walking_time, switching_time)
    self.transit_part = transit_route(path_type, target_time, early_penalty, late_penalty, O, D, ID_list, transit_link_list, transit_path_ID, transit_fare, 0, after_transit_walking_time, transit_time)

  def get_travel_time(self, t, link_ID_list, dta):
    arrival_time = self.driving_part.get_travel_time(t, link_ID_list, dta)
    arrival_time += self.driving_part.get_travel_time(arrival_time, link_ID_list, dta)
    return arrival_time - t

class metro(base_path):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, O, D, ID_list, walking_time1, metro_time, walking_time2, metro_fee):
    super(metro, self).__init__(path_type, target_time, early_penalty, late_penalty, ID_list, O, D)
    self.walking_time1 = walking_time1 / UNIT_TIME
    self.walking_time2 = walking_time2 / UNIT_TIME
    self.metro_time = metro_time / UNIT_TIME
    self.metro_fee = metro_fee

  def get_metro_fee(self):
    return self.metro_fee

  def get_metro_inconvenience(self):
    return np.float(0)

  def get_travel_time(self, t, link_ID_list, dta):
    return self.walking_time1 + self.metro_time + self.walking_time2

  def get_cost(self, t, link_ID_list, dta):
    tt = self.get_travel_time(t, link_ID_list, dta)
    late_penalty = self.get_wrongtime_penalty(t + tt)
    return  T2M * tt + late_penalty + get_metro_fee() + self.get_metro_inconvenience()


def make_path(config):
  print "Creating route for:", config['mode']
  assert (config['mode'] in IMPLEMENT_TYPES)
  if config['mode'] == 'single_drive':
    assert (config['number_people'] == 1)
    p = driving_route(config['mode'], config['target_time'], config['early_penalty'], config['late_penalty'],
                      config['O'], config['D'], config['ID_list'],
                      config['link_list'], config['path_ID'], 1, config['parking_lot'], config['walking_time1'], config['walking_time2'])
  if config['mode'] == 'multiple_drive':
    assert(config['number_people'] > 1)
    p = driving_route(config['mode'], config['target_time'], config['early_penalty'], config['late_penalty'],
                      config['O'], config['D'],  config['ID_list'],
                      config['link_list'], config['path_ID'], config['number_people'], config['parking_lot'], config['walking_time1'], config['walking_time2'])
  if config['mode'] == 'transit':
    p = transit_route(config['mode'], config['target_time'], config['early_penalty'], config['late_penalty'],
                      config['O'], config['D'], config['ID_list'],
                      config['link_list'], config['path_ID'], config['transit_fare'], config['walking_time1'], 
                      config['walking_time2'], config['transit_time'])
  if config['mode'] == 'pnr':
    p = park_ride_route(config['mode'], config['target_time'], config['early_penalty'], config['late_penalty'],
                      config['O'], config['D'], config['ID_list'],  config['car_link_list'],
                      config['car_path_ID'], config['transit_link_list'], config['transit_path_ID'], config['parking_lot'],
                      config['transit_fare'], config['before_drive_walking_time'], config['switching_time'], config['after_transit_walking_time'],
                      config['transit_time']
                      )
  if config['mode'] == 'metro':
    p = metro(config['mode'], config['target_time'], config['early_penalty'], config['late_penalty'],
                      config['O'], config['D'], config['ID_list'], config['walking_time1'], config['metro_time'], config['walking_time2'], config['metro_fee'])

  return p


class Multimode_DUE():
  def __init__(self, nb):
    print "Init simulation"
    self.num_simulation_path = nb.config.config_dict['FIXED']['num_path']
    self.num_assign_interval = nb.config.config_dict['DTA']['max_interval']
    self.simulation_path_list = range(nb.config.config_dict['FIXED']['num_path'])

  def form_demand_for_simulation(self, path_list, path_matrix):
    assert(len(path_list) == path_matrix.shape[0])
    car_flow = np.zeros((self.num_simulation_path, self.num_assign_interval))
    truck_flow = np.zeros((self.num_simulation_path, self.num_assign_interval))
    for i, path in enumerate(path_list):
      # print type(path)
      if path.path_type == 'single_drive' or path.path_type == 'multiple_drive':
        # print "driving route"
        path_idx = self.simulation_path_list.index(path.path_ID)
        # print path_idx
        car_flow[path_idx, :] = path_matrix[i, :] / np.float(path.number_people)
      if path.path_type == 'pnr':
        # print "park and ride route"
        car_path_idx = self.simulation_path_list.index(path.driving_part.path_ID)
        car_flow[car_path_idx, :] = path_matrix[i, :]
        # path_idx = self.simulation_path_list.index(path.transit_part.path_ID)
        # truck_flow[path_idx, :] = path_matrix[i, :]
    truck_flow[2, :] = np.ones(self.num_assign_interval) * 10
    truck_flow[7, :] = np.ones(self.num_assign_interval) * 10
    return car_flow, truck_flow


  def get_simulation(self, car_flow, truck_flow, choice_dict):
    data_folder = '../data/input_files_small_multiclass'
    cache_folder = 'cache'
    nb = MNM_network_builder()
    nb.load_from_folder(data_folder)
    nb.update_demand_path(car_flow.flatten(order = 'F'), truck_flow.flatten(order = 'F'), choice_dict)
    nb.dump_to_folder(cache_folder)
    link_ID_list = list(map(lambda x: x.ID, nb.link_list))
    dta = MNMAPI.mcdta_api()
    dta.initialize(cache_folder)
    dta.register_links(link_ID_list)
    dta.run_whole()
    return dta

  def get_cost_matrix(self, dta):
    pass

  def get_Lambda_matrix(self, dta):
    pass

  def update_path_matrix(self, cost_matrix, path_matrix):
    pass