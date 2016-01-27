'''
This file contains the general algorithm for manipulating the final dataframe.
For a location (x,y,z), the location would have pollution concentration C and the rate
of source emission is Q

Hence, for a location (x,y,z), if influenced by multiple sources of pollution, 
C = a_0 * Q_0 + a_1 * Q_1 + a_2 * Q_2 + ... + a_n * Q_n, where a is the coefficeint 
calculated by a gaussian dispersion model and Q is the rate of emission from location n

Functions used:
a: uses the Gaussian dispersion model to return a coefficient for a location
check_sigma_y: calculate sigma_y in the gaussian dispersion model
check_sigma_z: calculate sigma_z in the gaussian dispersion model

Possible bug: 
there is a row of zeros, rendering the matrix impossible to solve 
either sigma_y or sigma_z ends up being zero, but this was avoided already

Be very careful when writing the dataframe to it, check whether the A and B actually
have their elements filled in properly.

Also make sure that the matrix has the proper dates. i.e. when you pass a dataframe 
into the matrix, that dataframe should only include one single date and one single kind
of pollutant.
'''


#return coefficients to each place and and source for ONE SINGLE MONTH
#if the matrix is written in the form Ax = B, where A is the coefficient, 
#B is the final pollutant concentration C, and x is the rate of emission Q

def matrix(df,pollutant):
    total_rows = df.count()

    A = np.empty([total_rows,total_rows])
    B = df.as_matrix(columns=df[pollutant])


    #This for loop is used to populate the matrix. 
    for i in range(1,total_rows+1): #c1, c2 ..., initial
    final = [df['lon'][index[i]],df['lat'][index[i]],df['alt'][index[i]]
        for j in range(1,total_rows+1): #q1, q2 ...
            init = [df['lon'][index[j]],df['lat'][index[j]],df['alt'][index[j]]
            coefficient = a(df['uwnd'][index[j]],df['vwnd'][index[j]],init[0],init[1], init[2],final[0],final[1],final[2])
            A[i][j] = coefficient

    #solve the matrix
    X = np.linalg.solve(A,B)
    #X is the solution, i.e. the concentration of sources, of different places
    #A is the coefficeints multiplying the sources, i.e. the weight of each source
    return {'X' = X, 'A' = A}


#Calculate the coefficient for source Q to place with concentration C
#d is the directio vector between source and receptor
#u is the wind vector
def a(u_x, u_y, init_lat, init_lon, init_z, final_lat, final_lon, final_z):
    #init[0] / final[0]: longitude
    #init[1] / final[1]: latitude
    #init[2] / final[2]: altitude
    
    #convert lat lon to cartesian coordinates
    dx = (final_lon-init_lon)*40000*cos((final_lat+init_lat)*pi/360)/360
    dy = (init_lat-final_lat)*40000/360

    #vector distance between initial and final location
    d = [dx, dy, (final_z - init_z)]
    #calculate y
    dot_product = u_x*d[0] + u_y*d[1]


    if (dot_product < 0):
        return 0 #if the wind blows in opposite direction of the displacement vector, return 0
    else:
        mag_u = sqrt(u_x**2 + u_y**2)
        mag_d = sqrt(d[0]**2 + d[1]**2)
        if (mag_d == 0):
            sigma_y = 90 #assuming sigma is classified as D - Neutral
            sigma_z = 5
        else:
            theta = arccos(dot_product/(mag_u*mag_d))
            y = d * sin(theta) # y displacement from place a to place b
            #sigma y and z
            downwind_x = d[0]
            sigma_y = check_sigma_y(mag_u,downwind_x)
            sigma_z = check_sigma_z(mag_u,downwind_x)

        #other value constants
        z = final_z
        H = init_z
        
        denominator = 2 * pi * sigma_y * sigma_z * u
        numerator = exp(-0.5*((y**2/sigma_y**2)*(z-H)**2/sigma_z**2))
        return numerator / denominator

#compute sigma_z
def check_sigma_z(wind_speed,downwind_x):
    wind = abs(wind_speed)
    if (wind < 2){          #A-B
        if(x<10000){
            return sigma((0.495+0.310)/2,downwind_x,(0.873+0.897)/2)
        } else {
            return sigma((0.606+0.523)/2,downwind_x,(0.851+0.840)/2)
        } 
    }else if (wind <3){     #B
        if(x<=10000){
            return sigma(0.310,downwind_x,0.897)
        } else{
            return sigma(0.523,downwind_x,0.840)
        } 
    }else if (wind < 5){    #C
        if(x<=10000){
            return sigma(0.197,downwind_x,0.908)
        } else{
            return sigma(0.285,downwind_x,0.867)
        } 
    }else if(wind < 6){     #C_D
        if(x<=10000){
            return sigma((0.197+0.122)/2,downwind_x,(0.908+0.916)/2)
        } else{
            return sigma((0.285+0.193)/2,downwind_x,(0.867+0.865)/2)
        } 
    }else{#D
        if(x<=10000){
            return sigma(0.122,downwind_x,0.916)
        }else{
            return sigma(0.193,downwind_x,0.865)
        } 
    }


#compute sigma_y
def check_sigma_y(wind_speed,downwind_x):
    wind = abs(wind_speed)
    if (wind < 2){          #A-B
        if(x<=100){
            return 0
        } else if (x<= 500){
            return sigma((0.0383+1.393)/2,downwind_x,(1.281+0.9467)/2)
        } else {
            return sigma((0.0002539+0.04936)/2,downwind_x,(2.089+1.114)/2)
        } 
    }else if (wind <3){     #B
        if(x<=100){
            return 0
        } else if (x<= 500){
            return sigma(1.393,downwind_x,0.9467)
        } else{
            return sigma(0.04936,downwind_x,1.114)
        } 
    }else if (wind < 5){    #C
        if(x<=100){
            return 0
        } else if (x<= 500){
            return sigma(0.1120,downwind_x,0.9100)
        } else if (x<=5000){
            return sigma(0.1014,downwind_x,0.926)
        }else{
            return sigma(0.1154,downwind_x,0.9109)
        } 
    }else if(wind < 6){     #C_D
        if(x<=100){
            return 0
        } else if (x<= 500){
            return sigma((0.1120+0.0856)/2,downwind_x,(0.9100+0.8650)/2)
        } else if (x<=5000){
            return sigma((0.1014+0.2591)/2,downwind_x,(0.926+0.6869)/2)
        }else{
            return sigma((0.1154+0.7368)/2,downwind_x,(0.9109+0.5642)/2)
        } 
    }else{#D
        if(x<=100){
            return 0
        } else if (x<= 500){
            return sigma(0.0856,downwind_x,0.8650)
        } else if (x<=5000){
            return sigma(0.2591,downwind_x,0.6869)
        }else{
            return sigma(0.7368,downwind_x,0.5642)
        } 
    }

def sigma(constant, distance, power):
    return constant * (distance ** power)




