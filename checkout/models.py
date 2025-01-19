
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Bekliyor'),
        ('completed', 'Tamamlandı'),
    ]

    table_number = models.IntegerField()  # Masa numarası
    items = models.JSONField()  # Sepetteki ürünler
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Toplam fiyat
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Sipariş durumu
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - Masa {self.table_number}"
class EndOfDayReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_orders = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)  # Rapor dosyasını kaydetmek için

    def __str__(self):
        return f"Gün Sonu Raporu - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"