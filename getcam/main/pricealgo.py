
def model1(vendor_price,days):
    
    if days == 1:
        final_price =  0.95 * vendor_price
        profit  = vendor_price * (-205/100)
        discount = 5
    elif days == 2:
        final_price = 1.876 * vendor_price
        profit  = vendor_price * (-124/100)
        discount = 7.5
    elif days == 3:
        final_price = 2.785 * vendor_price
        profit  = vendor_price * (-21.2/100)
        discount = 9 
    elif days == 4:
        final_price = 3.643 * vendor_price
        profit  = vendor_price * (64.3/100)
        discount = 15 
    elif days == 5:
        final_price = 4.451 * vendor_price
        profit  = vendor_price * (145/100)
        discount = 20 
    elif days == 6:
        final_price = 5.258 * vendor_price
        profit  = vendor_price * (226/100)
        discount = 20 
    elif days >= 7:
        final_price = 6.018 * vendor_price
        profit  = vendor_price * (302/100)
        discount = 25 
    
    # profit =final_price -  (days *  vendor_price)
    return final_price,profit,discount


print(model1(200,5))