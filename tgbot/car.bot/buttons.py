from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


data = {
    "🚗 Mercedes": [
        {"model": "Mercedes-Benz C-Class Sedan", "year": 2025, "price": "$48,450",  "image": "https://di-shared-assets.dealerinspire.com/legacy/rackspace/ldm-images/2021-Mercedes-Benz-C-Class-Sedan-hero.png"},
        {"model": "Mercedes-Benz GLC SUV",        "year": 2025, "price": "$49,250",  "image": "https://hips.hearstapps.com/hmg-prod/images/2023-mercedes-benz-glc-class-101-1654031496.jpg?crop=0.646xw:0.546xh;0.157xw,0.363xh&resize=2048:*"},
        {"model": "Mercedes-Benz S-Class Sedan",  "year": 2025, "price": "$117,750", "image": "https://gateauto.ru/upload/resize_cache/iblock/e6d/678_423_2/0bhxh6ollzf23nd1s3owjlwgmywfjkfh.webp"},
        {"model": "Mercedes-Benz GLE SUV",        "year": 2025, "price": "$62,250",  "image": "https://www.mbusa.com/content/dam/mb-nafta/us/myco/my26/gle-class/gle-suv/byo-options/2026-GLE-SUV-MP-006.jpg"},
        {"model": "Mercedes-Benz G-Class SUV",    "year": 2025, "price": "$148,250", "image": "https://h1.nu/1xqdA"}
    ],                                        # ✅ Mercedes listi yopildi
    "🚗 BMW": [
        {"model": "BMW 3 Series Sedan",  "year": 2025, "price": "$43,500",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/sixty/2019_BMW_330i_%28G20%29_sedan%2C_front_8.6.19.jpg/1280px-2019_BMW_330i_%28G20%29_sedan%2C_front_8.6.19.jpg"},
        {"model": "BMW X5 SUV",          "year": 2025, "price": "$65,700",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/2019_BMW_X5_xDrive30d_M_Sport_Auto_%28Front%29.jpg/1280px-2019_BMW_X5_xDrive30d_M_Sport_Auto_%28Front%29.jpg"},
        {"model": "BMW 7 Series Sedan",  "year": 2025, "price": "$97,300",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/2023_BMW_740i_%28G70%29_sedan_%282023-02-17%29_01.jpg/1280px-2023_BMW_740i_%28G70%29_sedan_%282023-02-17%29_01.jpg"},
        {"model": "BMW M5 Sedan",        "year": 2025, "price": "$119,500", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/2021_BMW_M5_Competition_%28F90%29_sedan_%282021-09-13%29_01.jpg/1280px-2021_BMW_M5_Competition_%28F90%29_sedan_%282021-09-13%29_01.jpg"},
        {"model": "BMW iX Electric SUV", "year": 2025, "price": "$87,250",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/BMW_iX_xDrive50_%28I20%29%2C_front_8.22.21.jpg/1280px-BMW_iX_xDrive50_%28I20%29%2C_front_8.22.21.jpg"}
    ],
    "🚗 Audi": [
        {"model": "Audi A4 Sedan",         "year": 2025, "price": "$44,300",  "image": "https://images.carexpert.com.au/resize/960/-/cms/v1/media/2022-02-2022-audi-a4-sedan-45-tfsi-quattro-s-line-hero.jpg"},
        {"model": "Audi Q5 SUV",           "year": 2025, "price": "$47,900",  "image": "https://cdn.motor1.com/images/mgl/2NQNvx/379:728:2263:2263/2025-audi-q5.webp"},
        {"model": "Audi A8 Sedan",         "year": 2025, "price": "$89,100",  "image": "https://wroom.ru/i/cars2/audi_a8_4.jpg"},
        {"model": "Audi Q7 SUV",           "year": 2025, "price": "$58,600",  "image": "https://cdn.motor1.com/images/mgl/eo74pA/s3/2027-audi-q7.jpg"},
        {"model": "Audi e-tron GT Electric", "year": 2025, "price": "$107,800", "image": "https://cdn.motor1.com/images/mgl/KNqRb/s3/audi-e-tron-gt-quattro.jpg"}
    ],  # ✅ Audi listi yopildi

    "🚗 Tesla": [
        {"model": "Tesla Model 3",         "year": 2025, "price": "$42,990",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/2023_Tesla_Model_3_%28Highland%29%2C_front_8.10.23.jpg/1280px-2023_Tesla_Model_3_%28Highland%29%2C_front_8.10.23.jpg"},
        {"model": "Tesla Model Y",         "year": 2025, "price": "$47,990",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/2023_Tesla_Model_Y_Long_Range_%28facelift%2C_Australia%29%2C_front_8.3.23.jpg/1280px-2023_Tesla_Model_Y_Long_Range_%28facelift%2C_Australia%29%2C_front_8.3.23.jpg"},
        {"model": "Tesla Model S",         "year": 2025, "price": "$89,990",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/2022_Tesla_Model_S_Long_Range_%28US%29%2C_front_8.29.22.jpg/1280px-2022_Tesla_Model_S_Long_Range_%28US%29%2C_front_8.29.22.jpg"},
        {"model": "Tesla Model X",         "year": 2025, "price": "$99,990",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2022_Tesla_Model_X_Long_Range_%28US%29%2C_front_8.29.22.jpg/1280px-2022_Tesla_Model_X_Long_Range_%28US%29%2C_front_8.29.22.jpg"},
        {"model": "Tesla Cybertruck",      "year": 2025, "price": "$79,990",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/2024_Tesla_Cybertruck_%28US%29%2C_front_left%2C_1.13.24.jpg/1280px-2024_Tesla_Cybertruck_%28US%29%2C_front_left%2C_1.13.24.jpg"}
    ],  # ✅ Tesla listi yopildi

    "🚗 Porsche": [
        {"model": "Porsche 911 Carrera",   "year": 2025, "price": "$115,850", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Porsche_911_Carrera_4S_%28992%29%2C_front_8.8.19.jpg/1280px-Porsche_911_Carrera_4S_%28992%29%2C_front_8.8.19.jpg"},
        {"model": "Porsche Cayenne SUV",   "year": 2025, "price": "$83,350",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/2023_Porsche_Cayenne_S_%28PO536%2C_facelift%29%2C_front_8.10.23.jpg/1280px-2023_Porsche_Cayenne_S_%28PO536%2C_facelift%29%2C_front_8.10.23.jpg"},
        {"model": "Porsche Macan SUV",     "year": 2025, "price": "$68,500",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/2024_Porsche_Macan_4_Electric_%28J1A%29%2C_front_8.3.24.jpg/1280px-2024_Porsche_Macan_4_Electric_%28J1A%29%2C_front_8.3.24.jpg"},
        {"model": "Porsche Panamera",      "year": 2025, "price": "$103,750", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/2024_Porsche_Panamera_4_E-Hybrid_%28G2_II%2C_Australia%29%2C_front_8.3.24.jpg/1280px-2024_Porsche_Panamera_4_E-Hybrid_%28G2_II%2C_Australia%29%2C_front_8.3.24.jpg"},
        {"model": "Porsche Taycan Electric", "year": 2025, "price": "$96,700",  "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/2022_Porsche_Taycan_%28Y1A%2C_facelift%2C_Australia%29%2C_front_8.3.22.jpg/1280px-2022_Porsche_Taycan_%28Y1A%2C_facelift%2C_Australia%29%2C_front_8.3.22.jpg"}
    ]   # ✅ Porsche listi yopildi
}                                          



brendlar = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🚘Mercades'), KeyboardButton(text='🚘BMW')] ,
    [KeyboardButton(text='🚘Audi'), KeyboardButton(text='🚘Tesla')] ,
    [KeyboardButton(text='🚘Porsche')] 
])


mercedes_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=data["🚗 Mercedes"][0]["model"])],
    [KeyboardButton(text=data["🚗 Mercedes"][1]["model"])],
    [KeyboardButton(text=data["🚗 Mercedes"][2]["model"])],
    [KeyboardButton(text=data["🚗 Mercedes"][3]["model"])],
    [KeyboardButton(text=data["🚗 Mercedes"][4]["model"])],
    [KeyboardButton(text="🔙Orqaga qaytish")]
])



BMW_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=data["🚗 BMW"][0]["model"])],
    [KeyboardButton(text=data["🚗 BMW"][1]["model"])],
    [KeyboardButton(text=data["🚗 BMW"][2]["model"])],
    [KeyboardButton(text=data["🚗 BMW"][3]["model"])],
    [KeyboardButton(text=data["🚗 BMW"][4]["model"])],
    [KeyboardButton(text="🔙Orqaga qaytish")]
])


Audi_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=data["🚗 Audi"][0]["model"])],
    [KeyboardButton(text=data["🚗 Audi"][1]["model"])],
    [KeyboardButton(text=data["🚗 Audi"][2]["model"])],
    [KeyboardButton(text=data["🚗 Audi"][3]["model"])],
    [KeyboardButton(text=data["🚗 Audi"][4]["model"])],
    [KeyboardButton(text="🔙Orqaga qaytish")]
])


Tesla_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=data["🚗 Tesla"][0]["model"])],
    [KeyboardButton(text=data["🚗 Tesla"][1]["model"])],
    [KeyboardButton(text=data["🚗 Tesla"][2]["model"])],
    [KeyboardButton(text=data["🚗 Tesla"][3]["model"])],
    [KeyboardButton(text=data["🚗 Tesla"][4]["model"])],
    [KeyboardButton(text="🔙Orqaga qaytish")]
])


Porsche_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=data["🚗 Porsche"][0]["model"])],
    [KeyboardButton(text=data["🚗 Porsche"][1]["model"])],
    [KeyboardButton(text=data["🚗 Porsche"][2]["model"])],
    [KeyboardButton(text=data["🚗 Porsche"][3]["model"])],
    [KeyboardButton(text=data["🚗 Porsche"][4]["model"])],
    [KeyboardButton(text="🔙Orqaga qaytish")]
])   
