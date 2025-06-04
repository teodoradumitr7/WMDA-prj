def get_user_input():
    print("\nIntroduceți detaliile mașinii:")
    return {
        'year': int(input("Anul (ex: 2018): ")),
        'km_driven': int(input("Km rulați: ")),
        'fuel': input("Tip combustibil (Diesel/Benzina): ")
    }