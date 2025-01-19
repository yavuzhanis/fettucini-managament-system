from django.core.management.base import BaseCommand
from django.utils import timezone
from checkout.models import EndOfDayReport
from checkout.views import generate_end_of_day_report
from django.shortcuts import redirect

class Command(BaseCommand):
    help = 'Gün sonu raporunu oluşturur'

    def handle(self, *args, **kwargs):
        # Gün sonu raporunu oluştur
        generate_end_of_day_report()

        self.stdout.write(self.style.SUCCESS('Gün Sonu Raporu başarıyla oluşturuldu.'))

        
