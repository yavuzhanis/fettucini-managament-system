# admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import (
    Order,
    EndOfDayReport,
)  # Order ve EndOfDayReport modellerini import ettik
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.urls import path
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.contrib import messages
from django.utils.html import format_html
from django.http import FileResponse
from datetime import datetime
from django.http import StreamingHttpResponse

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table_number",
        "status",
        "total_price",
        "complete_order_button",
        "report_file_link",  # `report_file` alanını bir metod ile göstereceğiz
    )
    list_filter = ("status",)
    ordering = ("table_number",)
    search_fields = ("table_number", "status")

    def complete_order_button(self, obj):
        """Admin panelinde her siparişin yanında bir buton gösterir."""
        url = reverse("complete_order", args=[obj.pk])
        return mark_safe(f'<a class="button" href="{url}">Siparişi Tamamla</a>')

    complete_order_button.short_description = "Siparişi Tamamla"

    def mark_orders_completed(self, request, queryset):
        """Seçilen siparişleri tamamlanmış olarak işaretler."""
        queryset.update(status="completed")

    mark_orders_completed.short_description = "Seçilen siparişleri tamamla"

    def report_file_link(self, obj):
        """Admin panelinde rapor dosyasının bağlantısını gösterir."""
        if obj.report_file:
            return mark_safe(
                f'<a href="{obj.report_file.url}" target="_blank">Raporu Görüntüle</a>'
            )
        return "Rapor Yok"

    report_file_link.short_description = "Rapor Dosyası"


@admin.register(EndOfDayReport)
class EndOfDayReportAdmin(admin.ModelAdmin):
    list_display = ("created_at", "total_orders", "total_sales", "report_file")
    change_list_template = "admin/reports/end_of_day_report_change_list.html"  # Özel şablon ekliyoruz

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "generate_report/",
                self.admin_site.admin_view(self.generate_report),
                name="generate_report",
            ),
            path(
                "download_report/",
                self.admin_site.admin_view(self.download_report),
                name="download_report",
            ),
        ]
        return custom_urls + urls

    def generate_report(self, request):
        """Gün Sonu Raporu Oluştur"""
        try:
            # Raporu oluşturmak için fonksiyonu çağırıyoruz
            generate_end_of_day_report()  # Bu fonksiyonun doğru bir şekilde tanımlandığından emin olun

            # Başarı mesajı ekle
            messages.success(request, "Gün Sonu Raporu başarıyla oluşturuldu.")
        except Exception as e:
            # Hata mesajı ekle
            messages.error(request, f"Rapor oluşturulurken hata oluştu: {e}")

        # Admin paneline yönlendirme
        return redirect("admin:index")

    def download_report(self, request):
        """Txt Raporunu İndir"""
        today = datetime.today().strftime("%Y-%m-%d")
        txt_filename = f"end_of_day_report_{today}.txt"
        txt_path = os.path.join(settings.MEDIA_ROOT, "reports", "reports", txt_filename)

        # Dosya mevcut mu kontrol et
        if not os.path.exists(txt_path):
            messages.error(request, f"Rapor dosyası bulunamadı: {txt_path}")
            return redirect("admin:index")

        def file_iterator(file_path, chunk_size=8192):
            """Dosya içeriğini chunk'lar halinde döndüren bir fonksiyon"""
            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    yield chunk

        try:
            # Dosyayı 'file_iterator' ile akışa alıyoruz
            response = StreamingHttpResponse(file_iterator(txt_path), content_type="text/plain")
            response['Content-Disposition'] = f'attachment; filename={txt_filename}'

            # İndirme başarılı olduğunda mesaj ekle
            messages.success(request, "Rapor başarıyla indirildi.")
              # JavaScript ile yönlendirme ekliyoruz
            

            # Admin paneline yönlendirme yap
            response['Location'] = redirect("admin:index").url 
            return response
        
        except Exception as e:
            messages.error(request, f"Dosya indirilemedi: {str(e)}")
            return redirect("admin:index")

    def report_file(self, obj):
        """Admin panelinde TXT raporu indirme linki"""
        return format_html(
            '<a class="button" href="{}">TXT Raporunu İndir</a>',
            reverse("admin:download_report"),  # URL'yi admin URL'ine yönlendirdik
        )

    report_file.short_description = "Rapor İndir"



def generate_end_of_day_report():
    report = EndOfDayReport.objects.filter(
        created_at__date=timezone.now().date()
    ).first()

    if report:
        # Raporun içeriğini oluştur
        report_content = (
            f"Rapor Tarihi: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        report_content += f"Toplam Sipariş Sayısı: {report.total_orders}\n"
        report_content += f"Toplam Satış Tutarı: {report.total_sales} TL\n"

        # Dosya kaydetmek için doğru dizin oluşturuluyor
        report_dir = os.path.join(settings.MEDIA_ROOT, "reports")
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)  # Dizin yoksa oluştur

        # Dosya ismi
        report_file_name = (
            f"end_of_day_report_{timezone.now().strftime('%Y-%m-%d')}.txt"
        )
        report_file_path = os.path.join("reports", report_file_name)

        # Dosyayı kaydetmek için FileSystemStorage kullanıyoruz
        fs = FileSystemStorage(location=report_dir)

        with fs.open(report_file_path, "w") as report_file:
            report_file.write(report_content)

        # Raporu kaydet
        report.report_file = report_file_path
        report.save()

        # Rapor başarıyla oluşturulduktan sonra admin paneline yönlendirme
        return redirect("admin:index")  # Admin paneline yönlendirme
