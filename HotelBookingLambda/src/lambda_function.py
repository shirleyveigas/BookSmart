import json
def get_price_per_head(city):
    prices = {
        'mumbai': 500,
        'delhi': 600,
        'banglore': 700,
        'hyderabad': 800,
        'goa': 900,
        'pune': 1000
    }
    
    return prices.get(city, 0)

valid_cities = ['mumbai', 'delhi', 'banglore', 'hyderabad','goa','pune']

available_dates = {
    '01/10/2024': True,
    '02/10/2024': True,
    '03/10/2024': True,
    '11/10/2024': True,
    '12/10/2024': True,
    '15/10/2024': True,
    '16/10/2024': True,
    '18/10/2024': True,
    '19/10/2024': True,
    '21/10/2024': True,
    '22/10/2024': True,
    '23/10/2024': True,
    '24/10/2024': True,
    '25/10/2024': True,
    '30/10/2024': True,
    '31/10/2024': True,
    '01/11/2024': True,
    '02/12/2024': True,
    '03/12/2024': True,
    '11/12/2024': True,
    '12/12/2024': True,
    '15/12/2024': True,
    '16/12/2024': True,
    '18/12/2024': True,
    '19/12/2024': True,
    '21/12/2024': True,
    '22/12/2024': True,
    '23/12/2024': True,
    '24/12/2024': True,
    '25/12/2024': True,
    '30/12/2024': True,
    
}

def validate(slots):
    if not slots['Location']:
        print("Inside Empty Location")
        return {
            'isValid': False,
            'violatedSlot': 'Location'
        }
    
    if slots['Location']['value']['originalValue'].lower() not in valid_cities:
        print("Not Valide location")
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': 'We currently support only {} as a valid destination.'.format(", ".join(valid_cities))
        }
    
    
    if not slots['CheckInDate']:
        return {
            'isValid': False,
            'violatedSlot': 'CheckInDate',
        }
        
    check_in_date = slots['CheckInDate']['value']['originalValue']
    day, month, year = map(int, check_in_date.split('/'))
    
    
    
    available_dates_for_month = [date for date, available in available_dates.items() if int(date.split('/')[1]) == month and available]
    if year < 2024 or month<10:
        error_message = 'The check-in date {} is not available for booking. Please enter a date in DD/10/2024.'.format(check_in_date)
    else:
        if check_in_date not in available_dates:
            error_message = 'The check-in date {} is not available for booking. Available dates  are {}: Choose from these dates {}'.format(check_in_date,"\n", "\n".join(available_dates_for_month))
        else:
            error_message = None
    
    if error_message:
        print("Not Available CheckInDate")
        return {
            'isValid': False,
            'violatedSlot': 'CheckInDate',
            'message': error_message
        }
    
    if not slots['Guests']:
        return {
            'isValid': False,
            'violatedSlot': 'Guests',
        }
        
    guests = slots['Guests']['value']['originalValue']
    guests_count = int(guests)
    
    if guests_count > 5:
        error_message = 'We Cannot Accomadate Guests of {} . We Can Have Guests Not More Than 5 Per Room.Try Again!.'.format(guests)
    else:
        error_message = None
    
    if error_message:
        print("Not Available Guests")
        return {
            'isValid': False,
            'violatedSlot': 'Guests',
            'message': error_message
        }
    
    
    if not slots['Nights']:
        return {
            'isValid': False,
            'violatedSlot': 'Nights'
        }
    nights_of_stay = slots['Nights']['value']['originalValue']
    nights_of_stay_count = int(nights_of_stay)
    
    if nights_of_stay_count > 30:
        error_message = 'The number of nights of stay {} cannot be more than a month(30 Days). Please enter a number of nights not more than 30 days.'.format(nights_of_stay)
    else:
        total_cost = nights_of_stay_count * 3000
        message = "Total cost for {} nights of stay is {}".format(nights_of_stay, total_cost)
        print(message)
        return {
            'isValid': True,
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Total cost for {} nights of stay is {}".format(nights_of_stay, total_cost)
                }
            ]
        }
    
   
        
    if not slots['RoomType']:
        return {
            'isValid': False,
            'violatedSlot': 'RoomType'
        }

    return {'isValid': True}

def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(slots)
    print(validation_result)
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": validation_result['violatedSlot']
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            if 'message' in validation_result:
                response["messages"] = [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
            else:
                if validation_result['violatedSlot'] == 'Location':
                    response["prompt"] = {
                        "contentType": "PlainText",
                        "content": "Please enter a valid city"
                    }
                elif validation_result['violatedSlot'] == 'CheckInDate':
                    response["prompt"] = {
                        "contentType": "PlainText",
                        "content": "Please enter a valid check-in date"
                    }
                elif validation_result['violatedSlot'] == 'Guests':
                    response["prompt"] = {
                        "contentType": "PlainText",
                        "content": "Please enter a valid number of guests"
                    }
                elif validation_result['violatedSlot'] == 'Nights':
                    response["prompt"] = {
                        "contentType": "PlainText",
                        "content": "Please enter a valid number of nights"
                    }
                elif validation_result['violatedSlot'] == 'RoomType':
                    response["prompt"] = {
                        "contentType": "PlainText",
                        "content": "Please enter a valid room type"
                    }
                else:
                    response["prompt"] = {
                        "contentType": "PlainText",
                        "content": "Please enter a valid value for {}".format(validation_result['violatedSlot'])
                    }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
        
    if event['invocationSource'] == 'FulfillmentCodeHook':
        # Add order in Database
        nights_of_stay = slots['Nights']['value']['originalValue']
        nights_of_stay_count = int(nights_of_stay)
        guests = slots['Guests']['value']['originalValue']
        guests_count = int(guests)
        city = slots['Location']['value']['originalValue'].lower()
        price_per_head = get_price_per_head(city)
        total_cost = nights_of_stay_count * price_per_head * guests_count
        message = "Total cost for {} nights of stay is {}".format(nights_of_stay, total_cost)
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Your Reservation is Placed!!.Your total cost for {} nights of stay in {} for {} guests is ₹{}.".format(nights_of_stay, city, guests, total_cost)
                }
            ]
        }
    
    return response