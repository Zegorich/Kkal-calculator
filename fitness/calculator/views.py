from django.http import HttpResponse
from django.shortcuts import render
from math import e as exp


class OneRepMaximum():
    def __init__(self, weight, reps):
        self.weight = weight
        self.reps = reps

    def BoydEpley(self):
        return round(self.weight*(1+self.reps/30), 2)

    def MattBrzycki(self):
        return round(self.weight * 36 / (37 - self.reps), 2)

    def McGlothin(self):
        return round(100 * self.weight / (101.3 - 2.67123 * self.reps), 2)

    def Lander(self):
        return round(100 * self.weight / (101.3 - 2.67123 * self.reps), 2)

    def Lombardi(self):
        return round(self.weight * self.reps ** 0.1, 2)

    def Mayhew(self):
        return round(self.weight * 100 / (52.2 + 41.9 * exp ** (-0.055 * self.reps)), 2)

    def OConner(self):
        return round(self.weight * (1 + 0.025 * self.reps), 2)

    def Wathan(self):
        return round(100 * self.weight / (48.8 + 53.8 * exp ** (-0.075 * self.reps)), 2)

    def Wendler(self):
        return round(self.weight * self.reps * 0.0333 + self.weight, 2)

    def AvgMaximum(self):
        return round((self.Wathan() + self.Wendler() +
                self.Mayhew() + self.OConner() +
                self.BoydEpley() + self.MattBrzycki() +
                self.McGlothin() + self.Lander() + self.Lombardi()) / 9, 2)


class DailyCaloriesIntake():
    def __init__(self, age, weight, height, sex, activity):
        self.age = age
        self. weight = weight
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

def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'index.html', context=context)


def one_rep_maximum(request):
    context = {
        'title': 'Одноповторный максимум',
        'maximum': '',
    }
    if request.POST:
        weight = float(request.POST['weight'])
        reps = float(request.POST['reps'])
        context['maximum'] = OneRepMaximum(weight, reps)
    return render(request, 'one_rep_maximum.html', context=context)

def daily_calories_intake(request):
    context = {
        'title': 'Суточное потребление калорий',
        'calories': '',
    }
    if request.POST:
        response = request.POST
        age = int(response['age'])
        weight = float(response['weight'])
        height = float(response['height'])
        sex = response['sex']
        activity = float(response['activity'])
        calories = DailyCaloriesIntake(age=age, weight=weight, height=height, sex=sex, activity=activity)
        context['calories'] = calories
    return render(request, 'daily_calories_intake.html', context=context)