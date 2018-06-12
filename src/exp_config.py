from models import *

parking_surge = 1.0

cbd_parking = parking_lot(10 * parking_surge, 105, 120, 30000)
d2_parking = parking_lot(3 * parking_surge, 106, 60, 50000)
d3_parking = parking_lot(3 * parking_surge, 107, 60, 50000)


target_time = 2880
early_penalty = 3.9 / 60.0 / 60.0 * 5.0
late_penalty = 15.2 / 60.0 / 60.0 * 5.0

METRO_FARE = 3.75 * 1.0
BUS_FARE = 2.75 * 1.0

BUS_FREQ = 15


##################################################################
#####          O1 to D1
##################################################################
single_driving_config = dict()
single_driving_config['mode'] = 'single_drive'
single_driving_config['target_time'] = target_time
single_driving_config['early_penalty'] = early_penalty
single_driving_config['late_penalty'] = late_penalty
single_driving_config['ID_list'] = [0, 0, 0]
single_driving_config['O'] = 1
single_driving_config['D'] = 1
single_driving_config['link_list'] = [101, 2, 10, 16, 105]
single_driving_config['path_ID'] = 0
single_driving_config['number_people'] = 1
single_driving_config['parking_lot'] = cbd_parking
single_driving_config['walking_time1'] = 0.0
single_driving_config['walking_time2'] = 60.0
p11000 = make_path(single_driving_config)

single_driving_config = dict()
single_driving_config['mode'] = 'single_drive'
single_driving_config['target_time'] = target_time
single_driving_config['early_penalty'] = early_penalty
single_driving_config['late_penalty'] = late_penalty
single_driving_config['ID_list'] = [0, 0, 1]
single_driving_config['O'] = 1
single_driving_config['D'] = 1
single_driving_config['link_list'] = [101, 1, 9, 15, 105]
single_driving_config['path_ID'] = 1
single_driving_config['number_people'] = 1
single_driving_config['parking_lot'] = cbd_parking
single_driving_config['walking_time1'] = 0
single_driving_config['walking_time2'] = 60.0
p11001 = make_path(single_driving_config)



multiple_driving_config = dict()
multiple_driving_config['mode'] = 'multiple_drive'
multiple_driving_config['target_time'] = target_time
multiple_driving_config['early_penalty'] = early_penalty
multiple_driving_config['late_penalty'] = late_penalty
multiple_driving_config['ID_list'] = [0, 1, 0]
multiple_driving_config['O'] = 1
multiple_driving_config['D'] = 1
multiple_driving_config['link_list'] = [101, 2, 10, 16, 105]
multiple_driving_config['path_ID'] = 0
multiple_driving_config['number_people'] = 2
multiple_driving_config['parking_lot'] = cbd_parking
multiple_driving_config['walking_time1'] = 0
multiple_driving_config['walking_time2'] = 60.0
p11010 = make_path(multiple_driving_config)


metro_config = dict()
metro_config['mode'] = 'metro'
metro_config['target_time'] = target_time
metro_config['early_penalty'] = early_penalty 
metro_config['late_penalty'] = late_penalty
metro_config['O'] = 1
metro_config['D'] = 1
metro_config['ID_list'] = [1, 0, 0]
metro_config['walking_time1'] = 60.0
metro_config['metro_time'] = 40.0 * 60.0
metro_config['walking_time2'] = 60.0
metro_config['metro_fee'] = METRO_FARE
p11100 = make_path(metro_config)


pnr_config = dict()
pnr_config['mode'] = 'pnr'
pnr_config['target_time'] = target_time
pnr_config['early_penalty'] = early_penalty
pnr_config['late_penalty'] = late_penalty
pnr_config['ID_list'] = [2, 0, 0]
pnr_config['O'] = 1
pnr_config['D'] = 1
pnr_config['car_link_list'] = [101, 1, 106]
pnr_config['car_path_ID'] = 8
pnr_config['transit_link_list'] = [9, 15, 106]
pnr_config['transit_path_ID'] = -1
pnr_config['parking_lot'] = d2_parking
pnr_config['transit_fare'] = BUS_FARE
pnr_config['before_drive_walking_time'] = 60.0
pnr_config['switching_time'] = 60.0
pnr_config['after_transit_walking_time'] = 60.0
pnr_config['transit_time'] = BUS_FREQ / 2 * 60.0
p11200 = make_path(pnr_config)

pnr_config = dict()
pnr_config['mode'] = 'pnr'
pnr_config['target_time'] = target_time
pnr_config['early_penalty'] = early_penalty
pnr_config['late_penalty'] = late_penalty
pnr_config['ID_list'] = [2, 0, 1]
pnr_config['O'] = 1
pnr_config['D'] = 1
pnr_config['car_link_list'] = [101, 2, 8, 5, 3, 106]
pnr_config['car_path_ID'] = 9
pnr_config['transit_link_list'] = [9, 15, 105]
pnr_config['transit_path_ID'] = -1
pnr_config['parking_lot'] = d2_parking
pnr_config['transit_fare'] = BUS_FARE
pnr_config['before_drive_walking_time'] = 60.0
pnr_config['switching_time'] = 60.0
pnr_config['after_transit_walking_time'] = 60.0
pnr_config['transit_time'] = BUS_FREQ / 2 * 60.0
p11201 = make_path(pnr_config)


pnr_config = dict()
pnr_config['mode'] = 'pnr'
pnr_config['target_time'] = target_time
pnr_config['early_penalty'] = early_penalty
pnr_config['late_penalty'] = late_penalty
pnr_config['ID_list'] = [2, 1, 0]
pnr_config['O'] = 1
pnr_config['D'] = 1
pnr_config['car_link_list'] = [101, 1, 9, 107]
pnr_config['car_path_ID'] = 10
pnr_config['transit_link_list'] = [15, 105]
pnr_config['transit_path_ID'] = -1
pnr_config['parking_lot'] = d2_parking
pnr_config['transit_fare'] = BUS_FARE
pnr_config['before_drive_walking_time'] = 60.0
pnr_config['switching_time'] = 60.0
pnr_config['after_transit_walking_time'] = 60.0
pnr_config['transit_time'] = BUS_FREQ / 2 * 60.0
p11210 = make_path(pnr_config)

pnr_config = dict()
pnr_config['mode'] = 'pnr'
pnr_config['target_time'] = target_time
pnr_config['early_penalty'] = early_penalty
pnr_config['late_penalty'] = late_penalty
pnr_config['ID_list'] = [2, 1, 1]
pnr_config['O'] = 1
pnr_config['D'] = 1
pnr_config['car_link_list'] = [101, 2, 10, 14, 12, 107]
pnr_config['car_path_ID'] = 11
pnr_config['transit_link_list'] = [15, 105]
pnr_config['transit_path_ID'] = -1
pnr_config['parking_lot'] = d3_parking
pnr_config['transit_fare'] = BUS_FARE
pnr_config['before_drive_walking_time'] = 60.0
pnr_config['switching_time'] = 60.0
pnr_config['after_transit_walking_time'] = 60.0
pnr_config['transit_time'] = BUS_FREQ / 2 * 60.0
p11211 = make_path(pnr_config)

##################################################################
#####          O3 to D1
##################################################################

single_driving_config = dict()
single_driving_config['mode'] = 'single_drive'
single_driving_config['target_time'] = target_time
single_driving_config['early_penalty'] = early_penalty
single_driving_config['late_penalty'] = late_penalty
single_driving_config['ID_list'] = [0, 0, 0]
single_driving_config['O'] = 3
single_driving_config['D'] = 1
single_driving_config['link_list'] = [103, 7, 10, 16, 105]
single_driving_config['path_ID'] = 3
single_driving_config['number_people'] = 1
single_driving_config['parking_lot'] = cbd_parking
single_driving_config['walking_time1'] = 0.0
single_driving_config['walking_time2'] = 60.0
p31000 = make_path(single_driving_config)

single_driving_config = dict()
single_driving_config['mode'] = 'single_drive'
single_driving_config['target_time'] = target_time
single_driving_config['early_penalty'] = early_penalty
single_driving_config['late_penalty'] = late_penalty
single_driving_config['ID_list'] = [0, 0, 1]
single_driving_config['O'] = 3
single_driving_config['D'] = 1
single_driving_config['link_list'] = [103, 5, 3, 9, 15, 105]
single_driving_config['path_ID'] = 4
single_driving_config['number_people'] = 1
single_driving_config['parking_lot'] = cbd_parking
single_driving_config['walking_time1'] = 0.0
single_driving_config['walking_time2'] = 60.0
p31001 = make_path(single_driving_config)


multiple_driving_config = dict()
multiple_driving_config['mode'] = 'multiple_drive'
multiple_driving_config['target_time'] = target_time
multiple_driving_config['early_penalty'] = early_penalty
multiple_driving_config['late_penalty'] = late_penalty
multiple_driving_config['ID_list'] = [0, 1, 0]
multiple_driving_config['O'] = 3
multiple_driving_config['D'] = 1
multiple_driving_config['link_list'] = [103, 7, 10, 16, 105]
multiple_driving_config['path_ID'] = 3
multiple_driving_config['number_people'] = 2
multiple_driving_config['parking_lot'] = cbd_parking
multiple_driving_config['walking_time1'] = 0.0
multiple_driving_config['walking_time2'] = 60.0
p31010 = make_path(multiple_driving_config)


# metro_config = dict()
# metro_config['mode'] = 'metro'
# metro_config['target_time'] = target_time
# metro_config['early_penalty'] = early_penalty 
# metro_config['late_penalty'] = late_penalty
# metro_config['O'] = 3
# metro_config['D'] = 1
# metro_config['ID_list'] = [1, 0, 0]
# metro_config['walking_time1'] = 40
# metro_config['metro_time'] = 100
# metro_config['walking_time2'] = 30
# metro_config['metro_fee'] = 5
# p31100 = make_path(metro_config)


transit_config = dict()
transit_config['mode'] = 'transit'
transit_config['target_time'] = target_time
transit_config['early_penalty'] = early_penalty
transit_config['late_penalty'] = late_penalty
transit_config['ID_list'] = [1, 1, 0]
transit_config['O'] = 3
transit_config['D'] = 1
transit_config['link_list'] = [102, 3, 9, 15, 105]
transit_config['path_ID'] = -1
transit_config['transit_fare'] = BUS_FARE
transit_config['walking_time1'] = 60.0
transit_config['walking_time2'] = 60.0
transit_config['transit_time'] = BUS_FREQ / 2 * 60.0
p31110 = make_path(transit_config)


pnr_config = dict()
pnr_config['mode'] = 'pnr'
pnr_config['target_time'] = target_time
pnr_config['early_penalty'] = early_penalty
pnr_config['late_penalty'] = late_penalty
pnr_config['ID_list'] = [2, 0, 0]
pnr_config['O'] = 3
pnr_config['D'] = 1
pnr_config['car_link_list'] = [103, 5, 3, 106]
pnr_config['car_path_ID'] = 12
pnr_config['transit_link_list'] = [9, 15, 105]
pnr_config['transit_path_ID'] = -1
pnr_config['parking_lot'] = d2_parking
pnr_config['transit_fare'] = BUS_FARE
pnr_config['before_drive_walking_time'] = 60.0
pnr_config['switching_time'] = 60.0
pnr_config['after_transit_walking_time'] = 60.0
pnr_config['transit_time'] = BUS_FREQ / 2 * 60.0
p31200 = make_path(pnr_config)

##################################################################
#####          O4 to D1
##################################################################

single_driving_config = dict()
single_driving_config['mode'] = 'single_drive'
single_driving_config['target_time'] = target_time
single_driving_config['early_penalty'] = early_penalty
single_driving_config['late_penalty'] = late_penalty
single_driving_config['ID_list'] = [0, 0, 0]
single_driving_config['O'] = 4
single_driving_config['D'] = 1
single_driving_config['link_list'] = [104, 13, 16, 105]
single_driving_config['path_ID'] = 5
single_driving_config['number_people'] = 1
single_driving_config['parking_lot'] = cbd_parking
single_driving_config['walking_time1'] = 0.0
single_driving_config['walking_time2'] = 60.0
p41000 = make_path(single_driving_config)

single_driving_config = dict()
single_driving_config['mode'] = 'single_drive'
single_driving_config['target_time'] = target_time
single_driving_config['early_penalty'] = early_penalty
single_driving_config['late_penalty'] = late_penalty
single_driving_config['ID_list'] = [0, 0, 1]
single_driving_config['O'] = 4
single_driving_config['D'] = 1
single_driving_config['link_list'] = [104, 12, 15, 105]
single_driving_config['path_ID'] = 6
single_driving_config['number_people'] = 1
single_driving_config['parking_lot'] = cbd_parking
single_driving_config['walking_time1'] = 0.0
single_driving_config['walking_time2'] = 60.0
p41001 = make_path(single_driving_config)



multiple_driving_config = dict()
multiple_driving_config['mode'] = 'multiple_drive'
multiple_driving_config['target_time'] = target_time
multiple_driving_config['early_penalty'] = early_penalty
multiple_driving_config['late_penalty'] = late_penalty
multiple_driving_config['ID_list'] = [0, 1, 0]
multiple_driving_config['O'] = 4
multiple_driving_config['D'] = 1
multiple_driving_config['link_list'] = [104, 13, 16, 105]
multiple_driving_config['path_ID'] = 5
multiple_driving_config['number_people'] = 2
multiple_driving_config['parking_lot'] = cbd_parking
multiple_driving_config['walking_time1'] = 0.0
multiple_driving_config['walking_time2'] = 60.0
p41010 = make_path(multiple_driving_config)



pnr_config = dict()
pnr_config['mode'] = 'pnr'
pnr_config['target_time'] = target_time
pnr_config['early_penalty'] = early_penalty
pnr_config['late_penalty'] = late_penalty
pnr_config['ID_list'] = [2, 0, 0]
pnr_config['O'] = 4
pnr_config['D'] = 1
pnr_config['car_link_list'] = [104, 12, 107]
pnr_config['car_path_ID'] = 13
pnr_config['transit_link_list'] = [15, 105]
pnr_config['transit_path_ID'] = -1
pnr_config['parking_lot'] = d3_parking
pnr_config['transit_fare'] = BUS_FARE
pnr_config['before_drive_walking_time'] = 60.0
pnr_config['switching_time'] = 60.0
pnr_config['after_transit_walking_time'] = 60.0
pnr_config['transit_time'] = BUS_FREQ / 2 * 60.0
p41200 = make_path(pnr_config)



path_list = [p11000, p11001, p11010, p11100, p11200, p11201, p11210, p11211, 
             p31000, p31001, p31010, p31110, p31200,
             p41000, p41001, p41010, p41200]



choice_dict = dict()
choice_dict[1] = dict()
choice_dict[2] = dict()
choice_dict[3] = dict()
choice_dict[4] = dict()
choice_dict[5] = dict()
choice_dict[1][1] = 0
choice_dict[2][1] = 1
choice_dict[3][1] = 0
choice_dict[4][1] = 0
choice_dict[5][1] = 1
choice_dict[1][2] = 0
choice_dict[1][3] = 0
choice_dict[3][2] = 0
# choice_dict[3][3] = 0
choice_dict[4][3] = 0



trend = np.array([59857.4375, 69209.0000, 76571.9375, 83934.8750, 91297.8125, 98660.7500, 97057.6875, 95454.6250,
        93851.5625, 92248.5000, 88816.9375, 85385.3750, 81953.8125, 78522.2500, 77981.6875, 77441.1250])
trend = trend / np.sum(trend)


factor = 1.0
demand_dict = dict()
demand_dict[1] = dict()
demand_dict[3] = dict()
demand_dict[4] = dict()
demand_dict[1][1] = 15000.0 * trend * factor
demand_dict[3][1] = 10000.0 * trend * factor
demand_dict[4][1] = 5000.0 * trend * factor


ab_dict = dict()
ab_dict['a'] = dict()
ab_dict['a']['first'] = dict()
ab_dict['a']['first'][0] = 1    # drive
ab_dict['a']['first'][1] = 1.5    # transit
ab_dict['a']['first'][2] = 2.0    # pnr
ab_dict['a']['second'] = dict()
ab_dict['a']['second'][0] = dict()
ab_dict['a']['second'][1] = dict()
ab_dict['a']['second'][2] = dict()
ab_dict['a']['second'][0][0] = 1   # single drive
ab_dict['a']['second'][0][1] = 1   # multiple drive
ab_dict['a']['second'][1][0] = 1.5   # bus
ab_dict['a']['second'][1][1] = 1.5   # metro
ab_dict['a']['second'][2][0] = 2   # pnr1
ab_dict['a']['second'][2][1] = 2   # pnr2

ab_dict['b'] = dict()
ab_dict['b']['first'] = dict()
ab_dict['b']['first'][0] = 1    # drive
ab_dict['b']['first'][1] = 1    # transit
ab_dict['b']['first'][2] = 1    # pnr
ab_dict['b']['second'] = dict()
ab_dict['b']['second'][0] = dict()
ab_dict['b']['second'][1] = dict()
ab_dict['b']['second'][2] = dict()
ab_dict['b']['second'][0][0] = 1   # single drive
ab_dict['b']['second'][0][1] = 1   # multiple drive
ab_dict['b']['second'][1][0] = 1   # bus
ab_dict['b']['second'][1][1] = 1   # metro
ab_dict['b']['second'][2][0] = 1   # pnr1
ab_dict['b']['second'][2][1] = 1   # pnr2