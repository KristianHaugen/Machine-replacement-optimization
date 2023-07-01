import numpy as np
import pandas as pd


# calculations 
def calucations(nodes,df,n,I,max_age):
    f_t = np.zeros((max_age,n))

    #Set up order for calucaltions
    decisonYear = list(range(n-1))
    decisonYear.reverse()

    #Chain for optimal decision
    chain = []
    
    # DataFrame to store all values
    df_output = pd.DataFrame(columns= ["Stage","State","Keep","Replace","opt_value","Decision"])

    #Cacluate stages and find the optimcal decision for each state for each decision year.
    for i in decisonYear:   #Start at the last stage of the life cycle
        if i == max(decisonYear):
            for j in range(0,max_age):  #loop trough all posible ages that the machines can have e.i  0 - max age
                if nodes[j][i] == 1:    #check if the age of the machine i possible
                    if j == max_age-1:
                        calc_Replace_temp = df.iloc[0,1] + df.iloc[j+1,3] + df.iloc[1,3] - df.iloc[0,2]- I
                        f_t[j][i] = calc_Replace_temp #optimum value 
                        df_output = df_output.append({"Stage":i+1,"State":j+1,"Replace": calc_Replace_temp,"opt_value":calc_Replace_temp,"Decision":"R"},ignore_index=True)
                    else:
                        calc_Keep_temp = df.iloc[j+1,1] + df.iloc[j+2,3] - df.iloc[j+1,2]
                        calc_Replace_temp = df.iloc[0,1] + df.iloc[j+1,3] + df.iloc[1,3] - df.iloc[0,2] - I
                        optimal_value = max(calc_Keep_temp,calc_Replace_temp)

                        f_t[j][i] = max(calc_Keep_temp,calc_Replace_temp) # optimum value

                        if calc_Keep_temp > calc_Replace_temp:
                            decision = "K"
                        elif calc_Keep_temp == calc_Replace_temp:
                            decision = "R or K"
                        else:
                            decision = "R"

                        df_output = df_output.append({"Stage":i+1,"State":j+1,"Keep":calc_Keep_temp, "Replace":calc_Replace_temp,"opt_value":optimal_value,"Decision":decision},ignore_index=True)           
        else:
            for j in range(max_age-1):
                if nodes[j][i] == 1:
                    calc_Keep_temp = df.iloc[j+1,1]-df.iloc[j+1,2]+f_t[j+1][i+1]
                    calc_Replace_temp = df.iloc[0,1] + df.iloc[j+1,3] -df.iloc[0,2] - I + f_t[0][i+1]
                    optimal_value = max(calc_Keep_temp,calc_Replace_temp)
                    f_t[j][i] = max(calc_Keep_temp,calc_Replace_temp) # optimum value

                    if calc_Keep_temp > calc_Replace_temp:
                        decision = "K"
                    elif calc_Keep_temp == calc_Replace_temp:
                        decision = "R or K"
                    else:
                        decision =" R"
                    df_output = df_output.append({"Stage":i+1,"State":j+1,"Keep":calc_Keep_temp, "Replace":calc_Replace_temp,"opt_value":optimal_value,"Decision":decision},ignore_index=True)
   

    #chain for optimal decisions
    for stage in range(1,max(df_output["Stage"]+1)):
        #For first stage
        if stage == 1:
            stages = df_output.loc[df_output["Stage"]== stage]
            age = stages["State"].values[0]
            opt_decision = stages["Decision"].item().strip()
            chain.append(opt_decision)
        else:
            if chain[-1] == "R":
                age = 1
                stages = df_output.loc[(df_output["Stage"]==stage) & (df_output["State"]== age)]
                opt_decision = stages["Decision"].item()
                chain.append(opt_decision)
            elif chain[-1] == "R or K": # forces to keep in order to retive one possible solution
                age  =+ 1
                stages = df_output.loc[(df_output["Stage"]==stage) & (df_output["State"]==age)]
                opt_decision = stages["Decision"].item()
                chain.append(opt_decision)
            else:
                age =+ 1
                stages = df_output.loc[(df_output["Stage"]==stage) & (df_output["State"]==age)]
                opt_decision = stages["Decision"].item()
                chain.append(opt_decision)
    
    return df_output, chain