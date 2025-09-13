from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Standards(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('active', 'Aktiv'),
        ('draft', 'Entwurf'),
        ('deprecated', 'Veraltet'),
        ('withdrawn', 'Zurückgezogen'),
    ]
    
    # Type choices
    TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('norm', 'Norm'),
        ('guideline', 'Richtlinie'),
        ('specification', 'Spezifikation'),
        ('regulation', 'Verordnung'),
    ]
    
    # Core identification
    app_name = models.CharField(
        max_length=30, 
        blank=True, 
        choices=[(app, app) for app in settings.CUSTOM_APPS],
        verbose_name="Anwendungsbereich"
    )
    
    standard_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Normnummer",
        help_text="z.B. DIN EN ISO 9001:2015"
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name="Titel"
    )
    
    short_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Kurztitel"
    )
    
    # Classification
    category = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Kategorie"
    )
    
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='standard',
        verbose_name="Typ"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Status"
    )
    
    # Detailed information
    description = models.TextField(
        blank=True,
        verbose_name="Beschreibung"
    )
    
    scope = models.TextField(
        blank=True,
        verbose_name="Anwendungsbereich"
    )
    
    version = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Version"
    )
    
    publication_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Veröffentlichungsdatum"
    )
    
    valid_until = models.DateField(
        null=True,
        blank=True,
        verbose_name="Gültig bis"
    )
    
    # References and documents
    link = models.URLField(
        blank=True,
        verbose_name="Externer Link",
        help_text="Link zur offiziellen Dokumentation"
    )
    
    datasheet = models.FileField(
        upload_to='media/standards/datasheets/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],
        verbose_name="Datenblatt"
    )
    
    reference_documents = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        verbose_name="Referenzdokumente"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Erstellt am"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Aktualisiert am"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktiv"
    )
    
    class Meta:
        db_table = 'tbl_standards'
        verbose_name = "Standard/Norm"
        verbose_name_plural = "Standards/Normen"
        ordering = ['standard_number', 'publication_date']
        indexes = [
            models.Index(fields=['standard_number']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['publication_date']),
        ]
    
    def __str__(self):
        return f"{self.standard_number} - {self.title}"
    
    @property
    def is_current(self):
        """Prüft ob der Standard aktuell gültig ist"""
        from django.utils import timezone
        if self.valid_until:
            return self.valid_until >= timezone.now().date()
        return self.status == 'active'
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('standard_detail', kwargs={'pk': self.pk})
    
class Material(models.Model):
    """Material properties for fasteners"""
    name = models.CharField(max_length=50, unique=True)
    material_code = models.CharField(max_length=20, blank=True)
    youngs_modulus = models.FloatField(help_text="Young's modulus in GPa")
    tensile_strength = models.FloatField(help_text="Tensile strength in MPa")
    shear_strength = models.FloatField(help_text="Shear strength in MPa")
    density = models.FloatField(help_text="Density in g/cm³")
    corrosion_resistance = models.CharField(max_length=100, blank=True)
        
    def __str__(self):
        return f"{self.name} ({self.material_code})" if self.material_code else self.name

    class Meta:
        db_table = 'tbl_materials'
        ordering = ['name']
        verbose_name = 'Material'
        verbose_name_plural = 'Materialien'
        constraints = [
            models.UniqueConstraint(fields=['material_code'], name='unique_material_code')
        ]