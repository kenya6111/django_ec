from django.core.management.base import BaseCommand
import random
import string

from django_ec.models import PromotionCodeModel


class Command(BaseCommand):
    # python manage.py help <カスタムコマンド名> を実行すると表示されるメッセージ
    help = "Help message"

    def add_arguments(self, parser):
        # オプションをつけたい場合のみ必要
        pass

    def handle(self, *args, **options):
        # 具体的な処理内容
        generate_count=0
        while generate_count < 10:
            code = self.generate_random_code(7)
            if PromotionCodeModel.objects.filter(promote_code=code):
                continue
            else:
                promotion_code = PromotionCodeModel(promote_code=code,discount_amount=random.randint(100,1000))
                promotion_code.save()
                generate_count=generate_count+1
                print(f'Generated promotion code: {code}')

    def generate_random_code(self, length=7):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choices(letters, k=length))