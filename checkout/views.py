from django.shortcuts import render, redirect,get_object_or_404
from .forms import OrderForm
from .models import Order
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
from .models import Order, EndOfDayReport
from django.utils import timezone
import os
from django.conf import settings
from django.http import FileResponse
from datetime import date
from django.http import StreamingHttpResponse
from datetime import datetime
from django.utils.html import format_html
from django.urls import reverse

def checkout_view(request):
    if request.method == "POST":
        # JSON verisini al
        data = json.loads(request.body)
        table_number = data.get("table_number")
        cart_items = data.get("cart_items")

        if table_number and cart_items:
            # Sepet verisini ve masa numarasını kaydet
            total_price = sum(item["price"] for item in cart_items)

            # Sipariş oluşturma
            order = Order.objects.create(
                table_number=table_number,
                total_price=total_price,
                items=cart_items,  # Sepet verilerini kaydediyoruz
            )

            # Sipariş başarılı
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Geçersiz veri."})

    return JsonResponse(
        {"success": False, "message": "Yalnızca POST istekleri kabul edilir."}
    )

def complete_order(request):
    # Logic to complete the order
    return render(request, 'order_complete.html')


def complete_order_view(request, order_id):
    """Admin panelinde siparişi tamamla."""
    # Siparişi veritabanından al
    order = get_object_or_404(Order, id=order_id)
    
    # Siparişi tamamla
    order.status = 'completed'
    order.save()

    # Admin paneline başarı mesajı ekle
    messages.success(request, f"Sipariş #{order.id} başarıyla tamamlandı.")

    # Gün Sonu Raporu'nu Güncelle
    report, created = EndOfDayReport.objects.get_or_create(created_at__date=timezone.now().date())  # O günün raporunu al
    report.total_orders += 1  # Sipariş sayısını bir artır
    report.total_sales += order.total_price  # Toplam satışları güncelle
    report.save()

    # Sipariş tamamlandığında görüntülenecek bir sayfa (HTML şablonu)
    return render(request, 'checkout/order_complete.html', {'order': order})


def generate_end_of_day_report():
    report = EndOfDayReport.objects.filter(created_at__date=timezone.localtime().date()).first()

    if report:
        # Raporun içeriğini oluştur
        report_content = f"Rapor Tarihi: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_content += f"Toplam Sipariş Sayısı: {report.total_orders}\n"
        report_content += f"Toplam Satış Tutarı: {report.total_sales} TL\n"

        # Dosya kaydedilecek dizin
        report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        
        # Dizin yoksa oluştur
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        # Dosya ismi
        report_file_name = f"end_of_day_report_{timezone.now().strftime('%Y-%m-%d')}.txt"
        report_file_path = os.path.join('reports', report_file_name)

        # Dosya yoluna göre dosya açıyoruz ve içeriği yazıyoruz
        full_path = os.path.join(settings.MEDIA_ROOT, report_file_path)
        
        # Dosya yazma işlemi
        with open(full_path, 'w') as report_file:
            report_file.write(report_content)

        # Raporu kaydet
        report.report_file = report_file_path
        report.save()

        # Rapor başarıyla oluşturulduktan sonra admin paneline yönlendirme
        return redirect('admin:index')  # Admin paneline yönlendirme
