import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import random
from math import e as exp
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import permission_required


menu = [
    {'title': 'Home', 'url_name': 'calculator:home'},
    {'title': 'One rep maximum', 'url_name': 'calculator:one-rep-maximum'},
    {'title': 'Daily calories intake', 'url_name': 'calculator:daily-calories-intake'},
    {'title': 'My nutritions', 'url_name':'calculator:my-nutrition'},
    {'title': 'Products categories', 'url_name': 'calculator:categories'},
    {'title': 'Profile', 'url_name': 'calculator:profile'},
]

def my_func(request):
    import requests
    from bs4 import BeautifulSoup as bs
    from transliterate import translit

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    request = requests.get(r"https://health-diet.ru/table_calorie/", headers=headers)
    soup = bs(request.text, "html.parser")
    all_a = soup.find_all("a", class_="mzr-tc-group-item-href")

    for a in all_a[50::]:
        request_ = requests.get(r"https://health-diet.ru" + a["href"], headers=headers)
        soup_ = bs(request_.text, 'html.parser')
        trs = soup_.find_all('tr')
        all_a_ = []
        for tr in trs[1:]:
            all_a_.append(tr.findChild('a'))

        for product in all_a_:
            if product == None:
                continue
            request__ = requests.get(r'https://health-diet.ru' + product['href'], headers=headers)
            soup__ = bs(request__.text, 'html.parser')
            trs_ = soup__.find('table', class_='el-table').find_all('tr')
            nutrients = {}

            for tr_ in trs_[1:5]:
                tr_td = tr_.find_all('td')[1:]
                nutrients[tr_td[0].text] = tr_td[1].text.split()[0]

            text = product.text
            data = [text, nutrients, a.text]
            print(data)
            category_slug = translit(data[2], 'ru', reversed=True).lower().replace(' ', '-')
            category, created = Category.objects.get_or_create(
                name=data[2],
                defaults={'slug': category_slug}
            )

            product = Product(
                name=data[0],
                calories=float(data[1]["Калории"]),
                protein=float(data[1]['Белки']),
                fat=float(data[1]['Жиры']),
                carbohydrates=float(data[1]['Углеводы']),
                category=category
            )
            product.save()


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
        'menu': menu,
    }
    return render(request, 'calculator/index.html', context=context)


def one_rep_maximum(request):
    context = {
        'title': 'Одноповторный максимум',
        'maximum': '',
        'menu': menu,
    }
    if request.POST:
        weight = float(request.POST['weight'])
        reps = float(request.POST['reps'])
        context['maximum'] = OneRepMaximum(weight, reps)
    return render(request, 'calculator/one_rep_maximum.html', context=context)

def daily_calories_intake(request):
    context = {
        'title': 'Суточное потребление калорий',
        'calories': '',
        'menu': menu,
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
    return render(request, 'calculator/daily_calories_intake.html', context=context)
@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        first_name = request.POST.get('first-name', '')
        last_name = request.POST.get('last-name', '')
        age = request.POST.get('age', '')
        sex = request.POST.get('sex', '')
        current_weight = request.POST.get('current-weight', '')
        desired_weight = request.POST.get('desired-weight', '')
        telegram = request.GET.get('id')
        email = request.POST.get('email', '')
        if any([first_name, last_name, age, sex, current_weight, desired_weight, email]):
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if age:
                user.age = int(age) if age.isdigit() else None
            if sex:
                user.sex = sex
            if current_weight:
                user.current_weight = float(current_weight)
            if desired_weight:
                user.desired_weight = float(desired_weight)
            if telegram:
                user.telegram = telegram
            if email:
                user.email = email
            user.save()
            messages.success(request, 'Профиль успешно обновлён.')
        else:
            messages.error(request, 'Ошибка обновления профиля. Пожалуйста, заполните все поля правильно.')
        return redirect('/profile')
    context = {'user' : user,
               'menu' : menu,}
    return render(request, 'registration/profile.html', context=context)



class register_view(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("calculator:profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def categories(request):
    context = {
        'title': 'Каталог товаров',
        'menu': menu,
    }
    cats = Category.objects.all()
    context['cats'] = cats

    return render(request, 'calculator/categories.html', context=context)

def category(requests, cat_slug):
    context = {
        'title': 'Каталог товаров',
        'menu': menu,
    }

    products = Category.objects.get(slug=cat_slug).product_set.all()
    context['products'] = products

    return render(requests, 'calculator/products.html', context=context)

def product(requests, productid):
    p = Product.objects.get(pk=productid)
    context = context = {
        'title': p.name,
        'product': p,
        'menu': menu,
    }

    return render(requests, 'calculator/product.html', context=context)

@login_required(login_url='/profile')
def my_nutrition(request):
    context = {
        'menu': menu,
        'products': '',
    }

    user = request.user

    if request.POST:
        product_name = request.POST['product-search']
        weight = request.POST['weight']
        product_id = Product.objects.filter(name=product_name)[0].id
        meal = request.POST['meal']

        usrntrtn = UserNutrition.objects.filter(user_id=user.id, product_id=product_id)
        if usrntrtn:
            usrntrtn[0].weight += float(weight)
            usrntrtn[0].save()
        else:
            UserNutrition.objects.create(user_id=user.id, product_id=product_id, weight=weight, meal=meal)

    products = User.objects.get(username=user).usernutrition_set.all()
    if products:
        meals = {
            1: [],
            2: [],
            3: [],
            4: [],
        }
        for p in products:
            pr = Product.objects.get(pk=p.product_id)
            meals[p.meal].append([
                pr.name,
                round(float(pr.calories)/100*float(p.weight), 2),
                round(float(pr.protein)/100*float(p.weight), 2),
                round(float(pr.fat)/100*float(p.weight), 2),
                round(float(pr.carbohydrates)/100*float(p.weight), 2),
                p.weight])
        context['products'] = meals

    return render(request, 'calculator/my_nutrition.html', context=context)

# views.py
from django.http import JsonResponse
from .models import Product

def search_products(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))[:5]  # Ограничиваем до первых 5 совпадений
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
