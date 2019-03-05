#An example of filter function
vehicle_num = 'AP09BR4567'
Yr_List = [1980, 1988, 1990, 1992, 1993, 1998, 2002, 'AP09BR4567']
Leap_Years = list(filter(lambda leap_yrs: (leap_yrs == vehicle_num) , Yr_List))
print("Leap years after applying filter: " ,Leap_Years)