all_services = {
    "Adaptation of housing": [
        "Autonomy diagnosis at home",
        "Rolling shutter",
        "Secure shower",
        "Stair lift",
        "wall-hung toilet"
    ],
    "Financial Help": [
        "Financial aid assistance",
        "Ma Prime Adapt’",
        "Go out More",
        "Assistance in Returning Home After Hospitalization",
        "Energy check",
        "The APA"
    ],
    "Insurance and foresight": [
        "Mutual Health",
        "Funeral Convention Insurance",
        "Hospital insurance"
    ],
    "Energy saving": [
        "Boiler",
        "Water heater",
        "Insulation",
        "Heat pump"
    ],
    "Finances and credits": [
        "Redemption of credits"
    ],
    "Specialized housing": [
        "Senior service residences",
        "Family welcome",
        "Intergenerational shared accommodation",
        "Autonomy residence",
        "EHPAD"
    ],
    "Medical material": [
        "Suitable can opener",
        "Bath board",
        "Shower stool",
        "Compression stockings",
        "Bed support bar",
        "Walking canes"
    ],
    "Heritage": [
        "Donation during lifetime"
    ],
    "Health and wellbeing": [
        "Care manager",
        "Physiotherapist",
        "Lift chair",
        "Senior tablet"
    ],
    "Security": [
        "Shower exit mat",
        "Shower mat",
        "Smartvision",
        "Smoke detector",
        "Remote assistance",
        "Bright path"
    ],
    "Personal services": [
        "Transportation on demand",
        "Housekeeper",
        "Help with small jobs and gardening",
        "Carrying meals"
    ],
    "Social life and leisure": [
        "Adapted holidays",
        "Seniors on vacation program"
    ]
  }


if __name__ == "__main__":
    with open("categories.txt", "w") as f:
        for cat, services in all_services.items():
            f.write(f"Category:{cat}\n")
            for service in services:
                f.write(f"-{service}\n")
            f.write("#"*50 + "\n")