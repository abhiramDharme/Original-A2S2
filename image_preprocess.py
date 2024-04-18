#(300, 100) top left
#(790, 100) top right
#(300, 380) bottom left
#(790, 380) bottom right
#jwala circle (28.549072, 77.184548) (381, 157)
#sac circle (28.546758, 77.185148) (419, 218)
#himadri circle (28.544863, 77.194476)  (638, 171)
#entrance (28.545861, 77.196540) (673, 120)
# adch gate (28.539450, 77.198897) (789, 282)


import csv
import numpy as np

MULTIPLY = np.array([[-10349.3216, 21401.1892], [-28356.9694, -10614.5441]])
ADD = np.array([[-1355995.58, 1629000.4379]])

with open("images/geographical_coordinates.csv", 'r') as geographical_coordinates:
    reader = csv.reader(geographical_coordinates)
    with open("images/pixel_coordinates.csv", 'w') as pixel_coordinaates:
        writer = csv.writer(pixel_coordinaates)

        for row in reader:
            x,y = map(float, row)
            [[pixel_x, pixel_y]] = MULTIPLY @ np.array([x,y]) + ADD
            pixel_x = round(pixel_x)
            pixel_y = round(pixel_y)
            
            writer.writerow([pixel_x, pixel_y])