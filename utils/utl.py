from article.models import Article
import random
from django.core.exceptions import ObjectDoesNotExist
from user.models import CustomUser


def generate_articles():

    def generate_title(text_stuff):
        return ' '.join(text_stuff[random.randint(1, number_of_words)] for n in range(random.randint(1, 4)))[:50]

    with open('utils/generator.txt') as lorem_ipsum:
        text_stuff = lorem_ipsum.read().split()
        number_of_words = len(text_stuff) - 1
        for i in range(20):
            title = generate_title(text_stuff)
            try:
                Article.objects.get(title=title)
                while title in Article.objects.all().values_list('title'):
                    title = generate_title(text_stuff)
            except ObjectDoesNotExist:
                pass
            text = ' '.join(text_stuff[random.randint(1, number_of_words)] for i in range(random.randint(500, 1000)))
            new_article = Article.objects.create(title=title, text=text, author=CustomUser.objects.get(username='Admin'))
            new_article.save()


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
