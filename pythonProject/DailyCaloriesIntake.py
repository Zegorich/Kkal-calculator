class DailyCaloriesIntake():
    def __init__(self, age, weight, height, sex, activity):
        self.age = age
        self.weight = weight
        self.height = height
        self.sex = sex
        self.activity = activity

    def calculate_calories_intake(self):
        if self.sex == "male":
            return int((10 * self.weight + 6.25 * self.height - 5 * self.age + 5) * self.activity)
        elif self.sex == 'female':
            return int((10 * self.weight + 6.25 * self.height - 5 * self.age - 161) * self.activity)
        else:
            return None

    def cut(self):
        calories = self.calculate_calories_intake()
        return (int(calories * 0.85), int(calories * 0.9))

    def bulk(self):
        calories = self.calculate_calories_intake()
        return (int(calories * 1.1), int(calories * 1.15))