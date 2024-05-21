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