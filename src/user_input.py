# def get_user_input():
#     return {
#         'year': 2018,
#         'km_driven': 40000,
#         'mileage': 18.0,
#         'engine': 1200.0,
#         'max_power': 85.0,
#         'torque': 115.0,
#         'seats': 5,
#         'fuel': 'Petrol',
#         'transmission': 'Manual',
#         'owner': 'First Owner'
#     }

def get_user_input():
    print("\nIntroduceți detaliile mașinii:")
    return {
        'year': int(input("Anul (ex: 2018): ")),
        'km_driven': int(input("Km rulați: ")),
        'mileage': float(input("Consum (km/l): ")),
        'engine': float(input("Capacitate motor (cc): ")),
        'max_power': float(input("Putere maximă (bhp): ")),
        'torque': float(input("Cuplu estimat (Nm): ")),
        'seats': int(input("Număr locuri: ")),
        'fuel': input("Tip combustibil (Petrol/Diesel/CNG/LPG): "),
        'transmission': input("Transmisie (Manual/Automatic): "),
        'owner': input("Proprietar (First Owner/Second Owner/etc): ")
    }