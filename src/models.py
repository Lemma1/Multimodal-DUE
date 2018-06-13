import os
import numpy as np
from collections import OrderedDict
import sys
import MNMAPI
# change this folder to include the MNM_mcnb.py
sys.path.append("/home/lemma/Documents/MAC-POSTS/side_project/network_builder")
from MNM_mcnb import *
import gp
import shutil
import pickle
import time

# implemented 
IMPLEMENT_TYPES = ['single_drive', 'multiple_drive', 'transit', 'pnr', 'metro']

BUS_FREQ = 15
TRHOUGH_TRUCK_PER_INTERVAL = 100
T2M = 6.4 / 60.0 / 60.0 * 5.0
UNIT_TIME = np.float(5)
TAU_DEF = 1.0
FLOW_SCALAR = 10.0
CARPOOL_COST_MUL = 1.0
TRANSIT_INCON = 0.0
RNR_INCON =  0.0



''' Parking Lot object '''
class parking_lot():
  def __init__(self, base_price, link_ID, ave_parking_time, cap):
    self.base_price = base_price
    self.link_ID = link_ID
    self.ave_parking_time = ave_parking_time / UNIT_TIME
    self.cap = np.float(cap)

  def get_price(self):
    return self.base_price

  def get_cruise_time(self, t, dta):
    occ = dta.get_car_link_out_num(self.link_ID, t) / FLOW_SCALAR
    return self.ave_parking_time / (1 - occ / self.cap)


''' Interface of passenger path '''
class base_path(object):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, ID_list, O, D):
    self.target_time = target_time
    self.early_penalty = early_penalty
    self.late_penalty = late_penalty
    self.ID_list = ID_list
    self.O = O
    self.D = D
    self.path_type = path_type

  # return the generalized cost of the passenger path departing at time t
  def get_cost(self, t, link_ID_list, dta):
    raise Exception('Method in base class should not be called!')

  # return the travel time departing at time t
  def get_travel_time(self, t, link_ID_list, dta):
    raise Exception('Method in base class should not be called!')

  # return the late or early penalty
  def get_wrongtime_penalty(self, arrival_time):
    return np.maximum(self.late_penalty * (arrival_time - self.target_time), self.early_penalty * (self.target_time -arrival_time))

''' solo driving and carpool '''
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
      arrival_time += dta.get_car_link_tt(np.array([arrival_time]))[idx, 0]
    arrival_time += self.walking_time2
    arrival_time += self.parking_lot.get_cruise_time(arrival_time, dta) / UNIT_TIME
    return arrival_time - t

  def get_carpool_cost(self):
    return (np.float(self.number_people) - 1.0) * CARPOOL_COST_MUL

  def get_amortized_parkingfee(self):
    return self.parking_lot.get_price() / np.float(self.number_people)


  def get_cost(self, t, link_ID_list, dta):
    tt = self.get_travel_time(t, link_ID_list, dta)
    late_penalty = self.get_wrongtime_penalty(t + tt)
    return T2M * tt + late_penalty + self.get_carpool_cost() + self.get_amortized_parkingfee()

''' Bus '''
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
      arrival_time += dta.get_truck_link_tt(np.array([arrival_time]))[idx, 0]
    arrival_time += self.walking_time2
    return arrival_time - t

  def get_transit_fee(self):
    return self.transit_fare

  def get_transit_inconvenience(self):
    return np.float(TRANSIT_INCON)

  def get_cost(self, t, link_ID_list, dta):
    tt = self.get_travel_time(t, link_ID_list, dta)
    late_penalty = self.get_wrongtime_penalty(t + tt)
    return T2M * tt + late_penalty + self.get_transit_fee() + self.get_transit_inconvenience()

''' Park and ride '''
class park_ride_route(base_path):
  def __init__(self, path_type, target_time, early_penalty, late_penalty, O, D, ID_list, car_link_list, car_path_ID, 
                        transit_link_list, transit_path_ID, parking_lot, transit_fare, 
                        before_drive_walking_time, switching_time, after_transit_walking_time, transit_time):
    super(park_ride_route, self).__init__(path_type, target_time, early_penalty, late_penalty, ID_list, O, D)
    self.driving_part = driving_route(path_type, target_time, early_penalty, late_penalty, O, D, ID_list, car_link_list, car_path_ID, 1, parking_lot, before_drive_walking_time, switching_time)
    self.transit_part = transit_route(path_type, target_time, early_penalty, late_penalty, O, D, ID_list, transit_link_list, transit_path_ID, transit_fare, 0, after_transit_walking_time, transit_time)

  def get_pnr_inconvenience(self):
    return np.float(RNR_INCON)


  def get_travel_time(self, t, link_ID_list, dta):
    arrival_time = self.driving_part.get_travel_time(t, link_ID_list, dta)
    arrival_time += self.transit_part.get_travel_time(arrival_time, link_ID_list, dta)
    return arrival_time - t

  def get_cost(self, t, link_ID_list, dta):
    tt = self.get_travel_time(t, link_ID_list, dta)
    late_penalty = self.get_wrongtime_penalty(t + tt)
    return T2M * tt + late_penalty + self.driving_part.get_amortized_parkingfee() + self.transit_part.get_transit_fee() + self.get_pnr_inconvenience()

''' Metro '''
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
    return  T2M * tt + late_penalty + self.get_metro_fee() + self.get_metro_inconvenience()

''' This function is used to create a path object given the config file'''
# example of config file can be found in exp_config.py 
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


''' Implementation of MMDUE model '''
class Multimode_DUE():
  def __init__(self, nb):
    print "Init simulation"
    self.num_simulation_path = nb.config.config_dict['FIXED']['num_path']
    self.num_assign_interval = nb.config.config_dict['DTA']['max_interval']
    self.simulation_path_list = range(nb.config.config_dict['FIXED']['num_path'])
    self.nb = nb


  def init_path_matrix(self, path_list, demand_dict):
    path_matrix = np.zeros((len(path_list), self.num_assign_interval))
    for O in demand_dict.keys():
      for D in demand_dict[O].keys():
        tmp_path_list = list(filter(lambda x: x.O == O and x.D == D, path_list))
        assert (len(tmp_path_list) > 0)
        total_demand = demand_dict[O][D]
        for tmp_path in tmp_path_list:
          idx = path_list.index(tmp_path)
          path_matrix[idx, :] = total_demand / np.float(len(tmp_path_list))
    return path_matrix


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
    truck_flow[2, :] = np.ones(self.num_assign_interval) * (15.0 / BUS_FREQ) * 5 
    truck_flow[7, :] = np.ones(self.num_assign_interval) * TRHOUGH_TRUCK_PER_INTERVAL
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

  def get_cost_matrix(self, dta, path_list):
    cost_matrix = np.zeros((len(path_list), self.num_assign_interval))
    assign_freq = self.nb.config.config_dict['DTA']['assign_frq']
    link_ID_list = list(map(lambda x: x.ID, self.nb.link_list))
    for i in range(len(path_list)):
      passenger_path = path_list[i]
      # print passenger_path
      for t in range(self.num_assign_interval):
        cost_matrix[i, t] = passenger_path.get_cost(np.float(t * assign_freq), link_ID_list, dta)
    return cost_matrix

  def get_tt_matrix(self, dta, path_list):
    cost_matrix = np.zeros((len(path_list), self.num_assign_interval))
    assign_freq = self.nb.config.config_dict['DTA']['assign_frq']
    link_ID_list = list(map(lambda x: x.ID, self.nb.link_list))
    for i in range(len(path_list)):
      passenger_path = path_list[i]
      # print passenger_path
      for t in range(self.num_assign_interval):
        cost_matrix[i, t] = passenger_path.get_travel_time(np.float(t * assign_freq), link_ID_list, dta)
    return cost_matrix

  def get_Lambda_matrix(self, dta, path_list, path_matrix, demand_dict, ab_dict):
    Lambda_matrix = self.get_cost_matrix(dta, path_list)
    # print Lambda_matrix
    # for O in demand_dict.keys():
    #   for D in demand_dict[O].keys():
    #     tmp_path_list = list(filter(lambda x: x.O == O and x.D == D, path_list))
    #     assert (len(tmp_path_list) > 0)
    #     first_mode_list = 
    #     tmp_path_idx_list = list(map(lambda x: path_list.index(x), tmp_path_list))
    #     for tmp_path in tmp_path_list:
    #       idx = path_list.index(tmp_path)
    for i, path in enumerate(path_list):
      first_mode_path_list = list(filter(lambda x: x.O == path.O and x.D == path.D and x.ID_list[0] == path.ID_list[0], path_list))
      second_mode_path_list = list(filter(lambda x: x.O == path.O and x.D == path.D and x.ID_list[0] == path.ID_list[0] and x.ID_list[1] == path.ID_list[1], path_list))
      first_mode_path_idx_list = list(map(lambda x: path_list.index(x), first_mode_path_list))
      second_mode_path_idx_list = list(map(lambda x: path_list.index(x), second_mode_path_list))
      logh1 = safelog(np.sum(path_matrix[first_mode_path_idx_list, :], axis = 0))
      logh2 = safelog(np.sum(path_matrix[second_mode_path_idx_list, :], axis = 0))
      # print "logh1", logh1
      # print "logh2", logh2
      Lambda_matrix[i, :] += ((ab_dict['a']['first'][path.ID_list[0]] + logh1) / ab_dict['b']['first'][path.ID_list[0]]
                            - logh1 / ab_dict['b']['first'][path.ID_list[0]]
                            + (ab_dict['a']['second'][path.ID_list[0]][path.ID_list[1]] + logh2) / ab_dict['b']['second'][path.ID_list[0]][path.ID_list[1]])
    return Lambda_matrix

  def get_merit_gap(self, Lambda_matrix, path_matrix, path_list, demand_dict):
    gap = np.float(0)
    for O in demand_dict.keys():
      for D in demand_dict[O].keys():
        tmp_path_list = list(filter(lambda x: x.O == O and x.D == D, path_list))
        tmp_path_idx_list = list(map(lambda x: path_list.index(x), tmp_path_list))
        # print tmp_path_idx_list
        Pi = np.min(Lambda_matrix[tmp_path_idx_list, :], axis = 0)
        # print Pi
        gap += np.sum(path_matrix[tmp_path_idx_list, :] * (Lambda_matrix[tmp_path_idx_list, :] - Pi))
    return gap / np.sum(path_matrix)

  def update_path_matrix(self, Lambda_matrix, path_matrix, path_list, demand_dict, iter, m = 'direct'):
    LAMBDA = 0.1 / np.sqrt(iter + 1)
    new_path_matrix = np.zeros(path_matrix.shape)
    # tmp_target_matrix = path_matrix - TAU / np.sqrt(iter + 1) * Lambda_matrix
    for O in demand_dict.keys():
      for D in demand_dict[O].keys():
        tmp_path_list = list(filter(lambda x: x.O == O and x.D == D, path_list))
        tmp_path_idx_list = list(map(lambda x: path_list.index(x), tmp_path_list))
        for t in range(self.num_assign_interval):
          tau = 1.0 / (np.max(Lambda_matrix[tmp_path_idx_list, t]) - np.mean(Lambda_matrix[tmp_path_idx_list, t])) * TAU_DEF
          # tau = 400
          if m == 'direct':
            new_path_matrix[tmp_path_idx_list, t] = gp.get_projection(demand_dict[O][D][t], path_matrix[tmp_path_idx_list, t] - tau * Lambda_matrix[tmp_path_idx_list, t])
          if m == 'cvx':
            new_path_matrix[tmp_path_idx_list, t] = gp.solve_cvx(demand_dict[O][D][t], path_matrix[tmp_path_idx_list, t] - tau * Lambda_matrix[tmp_path_idx_list, t])
    new_path_matrix = np.maximum(new_path_matrix, 0.0)
    # return new_path_matrix * LAMBDA + (1-LAMBDA) * path_matrix
    return new_path_matrix

  def update_path_matrix2(self, Lambda_matrix, path_matrix, path_list, demand_dict, iter):
    LAMBDA = 0.2 / np.sqrt(iter + 1)
    new_path_matrix = np.zeros(path_matrix.shape)
    for O in demand_dict.keys():
      for D in demand_dict[O].keys():
        tmp_path_list = list(filter(lambda x: x.O == O and x.D == D, path_list))
        tmp_path_idx_list = list(map(lambda x: path_list.index(x), tmp_path_list))
        for t in range(self.num_assign_interval):
          path_idx = tmp_path_idx_list[np.argmin(Lambda_matrix[tmp_path_idx_list, t])]
          rest_path_idx = list(set(tmp_path_idx_list) - set([path_idx]))
          new_path_matrix[path_idx, t] = path_matrix[path_idx, t] + LAMBDA * path_matrix[rest_path_idx, t].sum(axis = 0)
          new_path_matrix[rest_path_idx, t] = (1 - LAMBDA) * path_matrix[rest_path_idx, t]
    new_path_matrix = np.maximum(new_path_matrix, 0.0)
    return new_path_matrix

  def solve(self, init_path_matrix, path_list, demand_dict, ab_dict, choice_dict, num_iters = 100, gd_method = 'GP', name = ''):
    path_matrix = init_path_matrix
    gap_record = list()
    dta_list = list()
    time_list = list()
    start = time.time()
    for i in range(num_iters):
      # print path_matrix
      car_flow, truck_flow = self.form_demand_for_simulation(path_list, path_matrix)
      dta = self.get_simulation(car_flow, truck_flow, choice_dict)
      Lambda_matrix = self.get_Lambda_matrix(dta, path_list, path_matrix, demand_dict, ab_dict)
      # print Lambda_matrix
      gap = self.get_merit_gap(Lambda_matrix, path_matrix, path_list, demand_dict)
      if gd_method == 'GP':
        path_matrix = self.update_path_matrix(Lambda_matrix, path_matrix, path_list, demand_dict, i)
      if gd_method == "MSA":
        path_matrix = self.update_path_matrix2(Lambda_matrix, path_matrix, path_list, demand_dict, i)
      if gd_method == 'GP2':
        path_matrix = self.update_path_matrix(Lambda_matrix, path_matrix, path_list, demand_dict, i, m = 'cvx')
      print i, gap
      gap_record.append(gap)
      dta_list.append(dta)
      end = time.time()
      time_list.append(end - start)

    car_flow, truck_flow = self.form_demand_for_simulation(path_list, path_matrix)
    dta = self.get_simulation(car_flow, truck_flow, choice_dict)
    cost_matrix = self.get_cost_matrix(dta, path_list)
    tt_matrix = self.get_tt_matrix(dta, path_list)
    Lambda_matrix = self.get_Lambda_matrix(dta, path_list, path_matrix, demand_dict, ab_dict)
    pickle.dump([path_matrix, Lambda_matrix, cost_matrix, tt_matrix, gap_record, time_list], open(gd_method + name + ".pickle", 'wb'))
    dta_list.append(dta)
    return path_matrix, dta_list, gap_record


def safelog(x):
  # print "safe log", x
  safe_x = np.maximum(x , 1e-10)
  return np.log(safe_x)