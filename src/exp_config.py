from models import *

cbd_parking = parking_lot(5)
d2_parking = parking_lot(1)
d3_parking = parking_lot(1)


target_time = 3600
early_penalty = 0.7
late_penalty = 10

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
single_driving_config['walking_time1'] = 3
single_driving_config['walking_time2'] = 3
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
single_driving_config['walking_time1'] = 3
single_driving_config['walking_time2'] = 3
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
multiple_driving_config['walking_time1'] = 3
multiple_driving_config['walking_time2'] = 3
p11010 = make_path(multiple_driving_config)


metro_config = dict()
metro_config['mode'] = 'metro'
metro_config['target_time'] = target_time
metro_config['early_penalty'] = early_penalty 
metro_config['late_penalty'] = late_penalty
metro_config['O'] = 1
metro_config['D'] = 1
metro_config['ID_list'] = [1, 0, 0]
metro_config['walking_time1'] = 40
metro_config['metro_time'] = 100
metro_config['walking_time2'] = 30
metro_config['metro_fee'] = 5
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
pnr_config['transit_fare'] = 5
pnr_config['before_drive_walking_time'] = 3
pnr_config['switching_time'] = 5
pnr_config['after_transit_walking_time'] = 1
pnr_config['transit_time'] = 2
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
pnr_config['transit_fare'] = 5
pnr_config['before_drive_walking_time'] = 3
pnr_config['switching_time'] = 5
pnr_config['after_transit_walking_time'] = 1
pnr_config['transit_time'] = 2
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
pnr_config['transit_fare'] = 5
pnr_config['before_drive_walking_time'] = 3
pnr_config['switching_time'] = 5
pnr_config['after_transit_walking_time'] = 1
pnr_config['transit_time'] = 2
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
pnr_config['transit_fare'] = 5
pnr_config['before_drive_walking_time'] = 3
pnr_config['switching_time'] = 5
pnr_config['after_transit_walking_time'] = 1
pnr_config['transit_time'] = 2
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
single_driving_config['walking_time1'] = 3
single_driving_config['walking_time2'] = 3
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
single_driving_config['walking_time1'] = 3
single_driving_config['walking_time2'] = 3
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
multiple_driving_config['walking_time1'] = 3
multiple_driving_config['walking_time2'] = 3
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
transit_config['transit_fare'] = 5
transit_config['walking_time1'] = 4
transit_config['walking_time2'] = 5
transit_config['transit_time'] = 40
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
pnr_config['transit_fare'] = 5
pnr_config['before_drive_walking_time'] = 3
pnr_config['switching_time'] = 5
pnr_config['after_transit_walking_time'] = 1
pnr_config['transit_time'] = 2
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
single_driving_config['walking_time1'] = 3
single_driving_config['walking_time2'] = 3
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
single_driving_config['walking_time1'] = 3
single_driving_config['walking_time2'] = 3
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
multiple_driving_config['walking_time1'] = 3
multiple_driving_config['walking_time2'] = 3
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
pnr_config['transit_fare'] = 5
pnr_config['before_drive_walking_time'] = 3
pnr_config['switching_time'] = 5
pnr_config['after_transit_walking_time'] = 1
pnr_config['transit_time'] = 2
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