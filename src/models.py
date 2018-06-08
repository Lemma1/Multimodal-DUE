import os
import numpy as np
from collections import OrderedDict

IMPLEMENT_TYPES = ['single_drive', 'multiple_drive', 'transit', 'pnr']

class parking_lot():
  def __init__(self, base_price):
    self.base_price = base_price

  def get_price(self):
    return self.base_path


# class link():
#   def __init__(self):
#     pass

#   def update_cc(self, in_cc, out_cc):
#     self.in_cc = in_cc
#     self.out_cc = out_cc

#   def get_tt(self, t):
#     return 0


class base_path(object):
  def __init__(self, target_time, early_penalty, late_penalty, ID_list, O, D):
    self.target_time = target_time
    self.early_penalty = early_penalty
    self.late_penalty = late_penalty
    self.ID_list = ID_list
    self.O = O
    self.D = D

  def get_cost():
    raise Exception('Method in base class should not be called!')

  def get_travel_time():
    raise Exception('Method in base class should not be called!')

  def get_wrongtime_penalty(self, arrival_time):
    return np.max(self.late_penalty * (arrival_time - self.target_time), self.early_penalty * (self.target_time -arrival_time))

class driving_route(base_path):
  def __init__(self, target_time, early_penalty, late_penalty, O, D, ID_list, link_list, path_ID, number_people, parking_lot, walking_time):
    assert(number_people >= 1)
    super(driving_route, self).__init__(target_time, early_penalty, late_penalty, ID_list, O, D)
    self.link_list = link_list
    self.path_ID = path_ID
    self.number_people = number_people
    self.parking_lot = parking_lot
    self.walking_time = walking_time

  def get_cost(self):
    return 0

  def get_carpool_cost(self):
    return self.number_people

  def get_amortized_parkingfee(self):
    return np.float(self.parking_fee) / np.float(number_people)

class transit_route(base_path):
  def __init__(self, target_time, early_penalty, late_penalty, O, D, ID_list, link_list, path_ID, transit_fare, walking_time, transit_waiting_time):
    super(transit_route, self).__init__(target_time, early_penalty, late_penalty, ID_list, O, D)
    self.link_list = link_list
    self.path_ID = path_ID
    self.transit_fare = transit_fare
    self.walking_time = walking_time
    self.transit_waiting_time = transit_waiting_time

class park_ride_route(base_path):
  def __init__(self, target_time, early_penalty, late_penalty, O, D, ID_list, car_link_list, car_path_ID, 
                        transit_link_list, transit_path_ID, parking_lot, transit_fare, 
                        before_drive_walking_time, switching_time, after_transit_walking_time, transit_waiting_time):
    super(park_ride_route, self).__init__(target_time, early_penalty, late_penalty, ID_list, O, D)
    self.driving_part = driving_route(target_time, early_penalty, late_penalty, O, D, car_link_list, car_path_ID, 1, parking_lot, before_drive_walking_time)
    self.transit_part = transit_route(target_time, early_penalty, late_penalty, O, D, transit_link_list, transit_path_ID, transit_fare, after_transit_walking_time, transit_waiting_time)


def make_path(config):
  print "Creating route for:", config['mode']
  assert (config['mode'] in IMPLEMENT_TYPES)
  if config['mode'] == 'single_drive':
    assert (config['number_people'] == 1)
    p = driving_route(config['target_time'], config['early_penalty'], config['late_penalty'], config['ID_list'],
                      config['O'], config['D'],
                      config['link_list'], config['path_ID'], 1, config['parking_lot'], config['walking_time'])
  if config['mode'] == 'multiple_drive':
    assert(config['number_people'] > 1)
    p = driving_route(config['target_time'], config['early_penalty'], config['late_penalty'], config['ID_list'],
                      config['O'], config['D'],
                      config['link_list'], config['path_ID'], config['number_people'], config['parking_lot'], config['walking_time'])
  return p


class Multimode_DUE():
  def __init__(self):
    print "Init simulation"
    self.num_simulation_path = None
    self.num_assign_interval = None
    self.simulation_path_list = None

  def form_demand_for_simulation(self, path_list, path_matrix):
    assert(len(path_list) == path_matrix.shape[0])
    car_flow = np.zeros((self.num_simulation_path, self.num_assign_interval))
    truck_flow = np.zeros((self.num_simulation_path, self.num_assign_interval))
    for i, path in enumerate(path_list):
      if type(path) is driving_route:
        print "driving route"
        path_idx = self.simulation_path_list.index(path.path_ID)
        car_flow[path_idx, :] = path_matrix[i, :] / np.float(path.number_people)
      if type(path) is transit_route:
        print "transit route"
        # path_idx = self.simulation_path_list.index(path.path_ID)
        # truck_flow[path_idx, :] = path_matrix[i, :]
      if type(path) is park_ride_route:
        print "park and ride route"
        car_path_idx = self.simulation_path_list.index(path.driving_part.path_ID)
        car_flow[car_path_idx, :] = path_matrix[i, :]
        # path_idx = self.simulation_path_list.index(path.transit_part.path_ID)
        # truck_flow[path_idx, :] = path_matrix[i, :]
    truck_flow[2, :] = np.ones(self.num_assign_interval) * 10
    truck_flow[7, :] = np.ones(self.num_assign_interval) * 10
    return car_flow, truck_flow


  def get_simulation(self):
    pass

  def get_cost_matrix(self, dta):
    pass

  def update_path_matrix(self, cost_matrix, path_matrix):
    pass