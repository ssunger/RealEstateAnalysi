import pandas as pd
from plotly import express as px

class Mortage_Calc():
    
    def __init__(self, value= 6*10**5, down_payemnt=6*10**4, rate=0.0295, years =  30,
                    gross_monthly_income= 100000/12, print_warning=1, maintanence_perc= 0.1):
        """
        value: total value of udnelying
        down_payemnt = down_ payment amount
        rate = anualized interest rate
        years = terms of loan
        gross_monthly_income = gross fmonthly income
        
        """
        self.value = value
        self.down_payemnt = down_payemnt
        self.loan = self.value - self.down_payemnt
        self.rate = rate
        self.years = years
        self.gross_monthly_income = gross_monthly_income
        self.maintanence_perc = maintanence_perc
        
        #check down payment amount and add values for isurance cost and update value accordingly
        self.min_down_payment_calc(print_warning)
        self.loan += self.insurance_premiume_calc()
        
        #calculate monthly int rate
        self.monthly_int_rate_calc()
        Monthly = self.Monthly_Cost()
        self.Calculate_total_paid()
        
    ################################################################################################
    def ret_2_dec_float(sef, x):
        return float("{0:.2f}".format(x))    
    
    ################################################################################################
    def GDS(self, costs_list):
        """
        Calcualtes GDS
        """
        self.GDS = sum(costs_list)/self.gross_monthly_income
        return self.ret_2_dec_float(self.GDS)

    def TDS(self, debt_list):
        """
        calculates TDS
        """
        self.debt_list = debt_list
        self.TDS = sum(debt_list)/self.gross_monthly_income
        
        return self.ret_2_dec_float(self.TDS)

    def LTV(self):
        """
        Calcualtes LTV (Loan to Value ratio)
        """
        self.LTV = self.loan/self.value
        return self.ret_2_dec_float(self.LTV)

    ################################################################################################
    ## insurance and downpayment calculations
    def min_down_payment_calc(self, print_q):
        """
        Calcualte minimum downpayment ammounts
        """
        
        if self.value <= 500000:
            min_down_payment= self.value*0.05
        if self.value > 500000:
            if self.value > 1000000:
                min_down_payment= self.value*0.2
            else:
                min_down_payment= 500000*0.05 + (self.value-500000)*0.1
    
        self.min_down_payment = self.ret_2_dec_float(min_down_payment)
        
        self.down_payment_too_low = 0
        if self.min_down_payment > self.down_payemnt:
            self.down_payment_too_low = 1
            if print_q == 1:
                print("not enough downpayment")
    
    def insurance_premiume_perc(self):
        """
        Add insurance premeium base don amount of down payment
        """
        ltv = self.LTV()
        if ltv <=0.8:
            return 0
        elif ltv > 0.8:
            if ltv > 0.9:
                return 0.04
            elif ltv >= 0.85:
                return 0.031
            return 0.028
                                
    def insurance_premiume_calc(self):
        """
        Calculate insurance premium amount
        """
        self.insurance_prem_perc = self.insurance_premiume_perc()
        self.insurance_premiume = self.loan*self.insurance_prem_perc
        return self.insurance_premiume
    
    def lawyer_cost(self):
        return self.value*(1+percentage_lawyer)


    ################################################################################################
    def monthly_int_rate_calc(self):
        """
        Cacluates monthly interest rate from annuale interest rate 
        """
        self.annual_int_rate = self.rate
        self.monthly_int_rate = self.annual_int_rate/12
        self.compounded_annual_int_rate =  (1 + self.monthly_int_rate)**12
        
    def Monthly_Cost(self):
        """
        Calculates cost monthly cost of loan
        """
        
        #calculate mmontlhy payment made based on monthly itnerest rate
        
        #self.monthly_payment = self.monthly_int_rate/(1 - (1+self.monthly_int_rate)**(-self.years*12))*(self.loan)
        self.monthly_payment = (self.monthly_int_rate*(1+self.monthly_int_rate)**(self.years*12))
        self.monthly_payment = self.monthly_payment/(((1+self.monthly_int_rate)**(self.years*12)) -1)*self.loan
        
        #calculate monthly maintanence cost and addas differnt cost variable
        self.monthly_maint = self.value*self.maintanence_perc/100
        self.Monthly_Cost_With_Maintanence = self.monthly_payment + self.monthly_maint
        
        return self.ret_2_dec_float(self.monthly_payment)

    ################################################################################################
    def Calculate_total_paid(self):
        """
        Calculate amount payed over entire life of the loan
        """
        #total cost ofjsut the loan repayment
        self.total_cost = self.monthly_payment*self.years*12
        
        #total cost with paying maintanence
        self.total_cost_with_maintanence = self.Monthly_Cost_With_Maintanence*self.years*12
        
        return self.ret_2_dec_float(self.total_cost)
    
    
    
    def Calculate_total_interest_paid(self):
        """
        Calculates total interest paid on mortage
        """
        
        self.total_interst_paid =  self.total_cost - self.value + self.insurance_premiume
        
        return self.ret_2_dec_float(self.total_interst_paid)
    
    def Calculate_total_interest_and_maintanence_paid(self):
        """
        Calculates total interest paid on mortage
        """
        
        self.total_interst_paid =  self.total_cost_with_maintanence  - self.value + self.insurance_premiume
        
        return self.ret_2_dec_float(self.total_interst_paid)

    ################################################################################################
    def cummulative_payment(self, period_check):
        """
        calcualte cummulative payments amount payed for loans of number of months/periods inputed as period_check
        """
        
        return self.ret_2_dec_float(self.monthly_payment*period_check)
    
    def cummulative_payment_with_maintanence(self, period_check):
        """
        calcualte cummulative payments amount payed for loans of number of months/periods inputed as period_check
        """
        
        return self.ret_2_dec_float(self.Monthly_Cost_With_Maintanence*period_check)

    def cummulative_interest(self, period_check):
        """
        calcualte cummulative interest payed for loans of number of months/periods inputed as period_check
        """
        
        cum_int = (self.loan*self.monthly_int_rate - self.monthly_payment)
        cum_int = cum_int*(((1+self.monthly_int_rate)**(period_check)) -1 )
        cum_int = cum_int/(self.monthly_int_rate) + self.monthly_payment*period_check
        
        return self.ret_2_dec_float(cum_int)
    
    def cummulative_non_principle(self, period_check):
        """
        calcualte cummulative interest payed for loans of number of months/periods inputed as period_check and
        add how much is payed for maintanence
        """
        
        cum_non_principle = self.cummulative_interest(period_check) + self.monthly_maint*period_check
        
        return self.ret_2_dec_float(cum_non_principle)

    def cummulative_equity(self, period_check):
        """
        calcualte cummulative equity payed for loans of number of months/periods inputed as period_check
        """
        cum_eq = self.monthly_payment*period_check - self.cummulative_interest(period_check)
        return self.ret_2_dec_float(cum_eq)
    
    ################################################################################################
    def equity_cum_payment_ratio(self, period_check, value, rate, years=30):
        return cummulative_equity(period_check, value, rate, 30)/(Monthly_Cost(value, rate, years)*period_check)

    def return_on_investment(self, period_check, percentage_payment_shared_down = 0.2,
                             percentage_payment_shared = 0.45, other_expenses = 700):
        
        return_val = self.cummulative_equity(period_check) + percentage_payment_shared_down*self.value
        cost_val = (self.monthly_payment*(1-percentage_payment_shared) +other_expenses)* period_check +\
        percentage_payment_shared_down*self.value
        return return_val/cost_val
    
    
class MortgageData:
    
    def __init__(self, start_val = 400000, incrament_val = 20000, num_inc = 20, start_val_dp = 40000,
                            incrament_val_dp = 10000, num_inc_dp = 10, maintanence_perc= 0.1,
                             years_use = 30, roomate= 0, int_rate =0.0295, real_estate_rate = 0.015,
                    annual_housing_market_growth_rate = [-0.02, 0, 0.015, 0.03, 0.045],
                    current_rent= 1500):
        monthly_pay = []
        monthly_pay_with_maintanence = []
        four_year_cum_eq = []
        four_year_cum_int =  []
        four_year_cum_tot = []
        two_year_cum_eq = []
        two_year_cum_int =[]
        two_year_cum_tot = []
        insurance_cost = []
        value_loan = []
        down_pay = []
        four_year_cum_tot_with_maint = []
        four_year_cum_tot_non_equity = []
        two_year_cum_tot_with_maint = []
        two_year_cum_tot_non_equity = []
        self.roomate_use = roomate
        self.int_rate = int_rate
        self.Annual_housing_market_growth_rate = annual_housing_market_growth_rate
        self.real_estate_rate = real_estate_rate
        self.current_rent= current_rent
        self.maintanence_fee = start_val*maintanence_perc
        
        self.start_val, self.incrament_val, self.num_inc = start_val, incrament_val, num_inc
        self.start_val_dp, self.incrament_val_dp, self.num_inc_dp =  start_val_dp,\
                        incrament_val_dp, num_inc_dp

        for i in [start_val+ incrament_val*j for j in range(num_inc)]:
            for k in [start_val_dp+ incrament_val_dp*t for t in range(num_inc_dp)]:
                morg = Mortage_Calc(value= i, down_payemnt=k, rate= self.int_rate,
                                    years= years_use, print_warning=0, 
                                    maintanence_perc= maintanence_perc)
                if morg.down_payment_too_low !=1:
                    monthly_pay.append(morg.monthly_payment)
                    monthly_pay_with_maintanence.append(morg.Monthly_Cost_With_Maintanence)
                    insurance_cost.append(morg.insurance_premiume)
                    four_year_cum_eq.append(morg.cummulative_equity(48))
                    four_year_cum_int.append(morg.cummulative_interest(48))
                    four_year_cum_tot.append(morg.cummulative_payment(48))
                    four_year_cum_tot_with_maint.\
                            append(morg.cummulative_payment_with_maintanence(48))
                    four_year_cum_tot_non_equity.append(morg.cummulative_non_principle(48))
                    two_year_cum_eq.append(morg.cummulative_equity(24))
                    two_year_cum_int.append(morg.cummulative_interest(24))
                    two_year_cum_tot.append(morg.cummulative_payment(24))
                    two_year_cum_tot_with_maint.\
                            append(morg.cummulative_payment_with_maintanence(24))
                    two_year_cum_tot_non_equity.append(morg.cummulative_non_principle(24))
                    value_loan.append(i)
                    down_pay.append(k)

        self.data = pd.DataFrame({"total_monthly_py" : monthly_pay,
                      "total_monthly_pay_with_maintanence" : monthly_pay_with_maintanence,
                      "monthly_pay": [num- self.roomate_use  for num in monthly_pay],
                      "monthly_pay_with_maintanence": [num- self.roomate_use\
                                                       for num in monthly_pay_with_maintanence],
                      "four_year_cum_eq": four_year_cum_eq,
                      "four_year_cum_int": four_year_cum_int,
                      "four_year_cum_non_principle": four_year_cum_tot_non_equity,
                      "four_year_cum_tot_with_maint": four_year_cum_tot_with_maint,
                      "four_year_cum_tot_with_maint_net": [i - self.roomate_use*48\
                                                           for i in four_year_cum_tot_with_maint],
                      "two_year_cum_eq": two_year_cum_eq,
                      "two_year_cum_int":two_year_cum_int,
                      "two_year_cum_non_principle":two_year_cum_tot_non_equity,
                      "two_year_cum_tot_with_maint": two_year_cum_tot_with_maint,
                      "two_year_cum_tot_with_maint_net": [i - self.roomate_use*24 \
                                                          for i in two_year_cum_tot_with_maint],
                      "insurance_cost": insurance_cost,
                      "value_loan": value_loan,
                      "down_pay": down_pay,
                      "two_year_tot": two_year_cum_tot,
                      "four_year_tot": four_year_cum_tot,
                      "two_year_cum_int_monthly":[num/24 for num in two_year_cum_int],
                       "four_year_cum_int_monthly": [num/48 for num in four_year_cum_int],
                      "two_year_cum_non_principle_monthly":[num/24 \
                                                    for num in two_year_cum_tot_non_equity],
                       "four_year_cum_non_principle_monthly": [num/48 \
                                                    for num in four_year_cum_tot_non_equity]})
        
        self.data["additional_costs"] = self.data.value_loan * self.real_estate_rate + 5000
        #for group in self.data.groupby(["down_pay", "value_loan"])
       
        ROI_vars = ["value_loan", "two_year_cum_eq", "four_year_cum_eq", "additional_costs",
                   "down_pay", "two_year_cum_tot_with_maint_net", "four_year_cum_tot_with_maint_net",
                   'two_year_cum_tot_with_maint', "four_year_cum_tot_with_maint"]
    
        #get rid of warnings
        import warnings
        warnings.filterwarnings('ignore')
       
        self.ROI_df = pd.DataFrame()
        for rate in self.Annual_housing_market_growth_rate:
            temp = self.data[ROI_vars]
            temp["housing_growth_rate"] = rate
             # get assumed value of the house in future
            temp["2_year_house_value"] = (1+rate)**2
            temp["2_year_house_value"] = temp["2_year_house_value"]*temp["value_loan"]
            temp["4_year_house_value"] = (1+rate)**4
            temp["4_year_house_value"] = temp["4_year_house_value"]*temp["value_loan"]
            # get change in value
            temp["2_year_house_value_change"] = temp["2_year_house_value"] - temp["value_loan"] 
            temp["4_year_house_value_change"] = temp["4_year_house_value"] - temp["value_loan"] 
            # get ROI
            
            ########################
            #### capital = capital held in asset = equity + downpay
            #### value = amoutn capital and value of home gained = capital + change in asset market rate 
            #### equivalent investment = amout of money that would be left if not spent on investment
            ####                       = invested capital + roomate pay 
            
            
            ## 2 Years
            temp["2_year_capital"] =  temp["two_year_cum_eq"] + \
                                      temp["down_pay"]
            temp["2_year_value"] = temp["2_year_capital"] + \
                                   temp["2_year_house_value_change"]
           
            
            ### Raw
            temp["2_year_invested_capital"] = temp["two_year_cum_tot_with_maint"] + \
                                              temp["down_pay"]

            temp["2_year_equivalent_invest"] =  temp["2_year_invested_capital"] -  \
                                            (self.current_rent
                                            - self.roomate_use)*24
            temp["2_year_ROI"] = self.annaulize_value(temp["2_year_value"] /\
                                                      temp["2_year_invested_capital"], 2)
            temp["2_year_ROI_equiv"] = self.annaulize_value(temp["2_year_value"] /\
                                                            (temp["2_year_equivalent_invest"]) , 2)
            
            ### Net
            temp["2_year_invested_capital_net"] = temp["two_year_cum_tot_with_maint_net"] +\
                                                  temp["down_pay"]
            temp["2_year_ROI_net"] = self.annaulize_value(temp["2_year_value"] / \
                                                          temp["2_year_invested_capital_net"], 2)
            temp["2_year_invested_capital_net"] = temp["two_year_cum_tot_with_maint_net"] +\
                                                  temp["down_pay"]
            temp["2_year_ROI_net_equiv"] = self.annaulize_value(temp["2_year_value"] /\
                                                          (temp["2_year_equivalent_invest"] -\
                                                           self.current_rent*24), 2) 
            
            ## 4 Years
            temp["4_year_capital"] =  temp["four_year_cum_eq"] + \
                                      temp["down_pay"]
            ### Net
            temp["4_year_value"] =  temp["4_year_house_value_change"]  + \
                                    temp["4_year_capital"]
            
            temp["4_year_invested_capital"] = temp["four_year_cum_tot_with_maint"] + \
                                                temp["down_pay"]
            
            temp["4_year_invested_capital_net"] = temp["four_year_cum_tot_with_maint_net"] + \
                                                  temp["down_pay"]
            temp["4_year_equivalent_invest"] =  temp["4_year_invested_capital"] - \
                                            (self.current_rent
                                            - self.roomate_use)*48
            temp["4_year_ROI_net"] = self.annaulize_value(temp["4_year_value"] / \
                                                          temp["4_year_invested_capital_net"], 4)
            temp["4_year_ROI_net_equiv"] = self.annaulize_value(temp["4_year_value"] / \
                                                          (temp["4_year_invested_capital_net"]-\
                                                           self.current_rent*48), 4)
            
            ### Raw

            temp["4_year_ROI"] = self.annaulize_value(temp["4_year_value"] /\
                                                      temp["4_year_invested_capital"], 4)
            temp["4_year_ROI_equiv"] = self.annaulize_value(temp["4_year_value"] /\
                                                          (temp["4_year_invested_capital"] - \
                                                           self.current_rent*48), 4) 
            #put together
            self.ROI_df = pd.concat([self.ROI_df,temp])
        
    def annaulize_value(self, value, n_years):
        return value**(1/n_years)
    def gen_sub_data(self, list_downpayment= [80000, 60000, 40000], return_sub_d = False):
        self.sub_data = self.data[self.data.down_pay.isin(list_downpayment)].copy()
        self.max_dp = max(list_downpayment)
        self.min_dp = min(list_downpayment)
        if return_sub_d:
            return self.sub_data
    
    def plot_x_value_loan(self, y_val, colour_val):
        
        return px.line(self.sub_data, x="value_loan", y = y_val, color= colour_val) 
    
    def plot_monthly_payments_breakdown(self, down_pay_use= 60000, 
                    breakdown_variables = ["monthly_pay", "two_year_cum_int_monthly", 
                                           "four_year_cum_int_monthly"],
                    roomate_use=False):
        self.gen_sub_data([down_pay_use])
        temp = self.sub_data.melt(id_vars="value_loan")
        temp = temp[temp.variable.isin(breakdown_variables)]
        return px.line(temp, x="value_loan", y = "value", color="variable")
    
    def plot_monthly_payment_percentage_breakdown(self, 
                    percentage_var = "two_year_cum_int_monthly", value_use = "600000"):
        
        temp = self.data[[percentage_var,  "monthly_pay_with_maintanence", "value_loan", "down_pay"]]
        temp["percentage_" + percentage_var + "_pay_per_month"] = temp[percentage_var] / temp["monthly_pay_with_maintanence"]
        return px.line(temp, x="value_loan", y = "percentage_" + percentage_var + "_pay_per_month", color="down_pay")
    
    def plot_percentage_downpayment_effect(self, x, dp):
        def demean(df, x, dp): 
            df = df[df["down_pay"] <= dp]
            df[ x + "_percentage_from_" + str(dp)] = (df[x] - df[x].min())*12 / (dp - df["down_pay"])
            return df
        temp = []
        for group in Mort.data.groupby("value_loan"):
            temp.append(demean(group[1],x , dp))
        temp_2 = pd.concat(temp)
        return px.line(temp_2, x="value_loan", y = x + "_percentage_from_" + str(dp), color= "down_pay")
    
    def plot_profit_metric(self, var_use, housing_rate):
        return px.line(self.ROI_df[self.ROI_df["housing_growth_rate"] == housing_rate],
                x= "value_loan",
                y= var_use,
                color= "down_pay")
    
    def plot_invested_capital(self, var_use):
        return px.line(self.ROI_df[self.ROI_df["housing_growth_rate"] == self.Annual_housing_market_growth_rate[0]],
                x= "value_loan",
                y= var_use,
                color= "down_pay")