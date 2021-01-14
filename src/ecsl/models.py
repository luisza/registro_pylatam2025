from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.


class PaymentOption(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    identification = models.CharField(
        max_length=30, verbose_name=_('Identificación'), null=True)
    tipo = models.CharField(max_length=255, verbose_name=_('Opción de envío'))
    email = models.EmailField()

    def __str__(self):
        return "%s -- %s (%s)" % (self.tipo, self.name, self.identification)

    class Meta:
        verbose_name = "Opción de pago"
        verbose_name_plural = "Opciones de pago"


class Gustos(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Gusto"
        verbose_name_plural = "Gustos"


class Encuentros_Anteriores(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Encuentro anterior"
        verbose_name_plural = "Encuentros anteriores"


class Inscription(models.Model):
    STATUS = (
        (0, 'Creado usuario'),
        (1, 'Pre-registo'),
        (2, 'Confirmado'),
    )
    gender_choice = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro')
    )

    PAIS = (
        ('Panamá', 'Panamá'),
        ('Costa Rica', 'Costa Rica'),
        ('Nicaragua', 'Nicaragua'),
        ('El Salvador', 'El salvador'),
        ('Guatemala', 'Guatemala'),
        ('Honduras', 'Honduras'),
        ('Belize', 'Belize'),
        ('Otro', 'Otro'),

    )

    CAMISETA = (
        ('S', 'S'),
        ('XS', 'XS'),
        ('M', 'M'),
        ('XM', 'XM'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    status = models.SmallIntegerField(choices=STATUS, default=0)
    identification = models.CharField(
        max_length=50, verbose_name=_('Identificación en su país/pasaporte'), null=True,
        help_text='Requisito para hospedarse en hotel')
    direccion_en_su_pais = models.CharField(
        max_length=250, verbose_name=_('Dirección en su país'), null=True, blank=True,
        help_text='Requisito para hospedarse en hotel')
    born_date = models.DateField(
        verbose_name=_('Fecha de Nacimiento'), null=True)
    institution = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_('Institución'))
    gender = models.CharField(max_length=9, choices=gender_choice, verbose_name=_(
        'Género'), default='Masculino')
    nationality = models.CharField(
        max_length=12, choices=PAIS,  verbose_name=_('Nacionalidad'))
    other_nationality = models.CharField(max_length=12, null=True, blank=True,
                                         verbose_name=_('Si marcó otro indique el país de procedencia'))
    encuentros = models.ManyToManyField(Encuentros_Anteriores, blank=True,
                                        help_text="Use ctrl o command en mac para seleccionar más de uno",
                                        verbose_name=_("Encuentros anteriores en los que ha participado"))
    alimentary_restriction = models.TextField(null=True, blank=True,
                                              verbose_name=_('¿Tiene alguna necesidad específica de alimentación y hospedaje o alguna condición de salud especial?.'))
    health_consideration = models.TextField(
        verbose_name=_('Condiciones de Salud'), null=True, blank=True)
    gustos_manias = models.ManyToManyField(Gustos,
                                           verbose_name="Por favor seleccione las opciones que correspondan a sus gustos, usos, costumbres, manías",
                                           help_text="Use ctrl o command en mac para seleccionar más de uno")
    observacion_gustos_manias = models.TextField(
        null=True, blank=True,
        verbose_name=_("Alguna otra observación sobre sus gustos, usos, costumbres y manías."))

    comentario_general = models.TextField(
        null=True, blank=True,
        verbose_name=_('Si tiene algún comentario y/o si quiere colaborar con la organización del 9° ECSL por favor comente en este espacio.'))

    camiseta = models.CharField(max_length=10, choices=CAMISETA)
    hora_de_llegada = models.CharField(
        max_length=150, null=True, blank=True)
    hora_de_salida = models.CharField(
        max_length=150, null=True, blank=True)
    medio_de_transporte = models.CharField(
        max_length=150, null=True, blank=True)
    lugar_de_arribo = models.CharField(
        max_length=150, null=True, blank=True)
    observaciones_del_viaje = models.TextField(
        null=True, blank=True, help_text="Si viaja en avión agregue el número de vuelo.")
    aparecer_en_participantes = models.BooleanField(default=True)
    event = models.ForeignKey('EventECSL', on_delete=models.CASCADE, null=True, verbose_name=_("Event"))

    @property
    def name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"


class Package(models.Model):
    name = models.CharField(max_length=40, default='',verbose_name=_("nombre"))
    description = models.CharField(max_length=100, default='', verbose_name=_("descripción"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('precio'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"


class Payment(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    option = models.ForeignKey(PaymentOption,
                               on_delete=models.CASCADE, verbose_name=_('Opción de pago'))
    codigo_de_referencia = models.CharField(max_length=40, verbose_name=_(
        'Id de transacción'), help_text="Identificación de transacción o código de referencia")
    invoice = models.FileField(upload_to="invoices/")
    confirmado = models.BooleanField(default=False)
    event = models.ForeignKey('EventECSL', on_delete=models.CASCADE, null=True, verbose_name=_("Event"))
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, verbose_name=_("Paquete"))


    @property
    def name(self):
        return self.user.get_full_name()

    def __str__(self):
        return "%s %s" % (self.user.get_full_name(), str(self.option))

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"


class Patrocinadores(models.Model):
    class Meta:
        verbose_name_plural = 'Patrocinador'
        verbose_name = 'Patrocinadores'

    TYPES = (
        ('gold', 'Oro'),
        ('Plate', 'Plata'),
        ('Bronce', 'Bronce'),
    )
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    web = models.URLField(verbose_name=_('Web'))
    logo = models.ImageField(verbose_name=_('logo'), upload_to='logos/')
    patrocin = models.SmallIntegerField(choices=TYPES)
    event = models.ManyToManyField('EventECSL', verbose_name=_("Event"))


class Becas(models.Model):
    ESTADOS = (
        (0, 'Solicitada'),
        (1, 'Aprobada'),
        (2, 'Rechazada')

    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    razon = models.TextField(
        verbose_name="Dinos porqué deberíamos darte la beca")
    aportes_a_la_comunidad = models.TextField(
        verbose_name="¿Cúales son tus aportes a la comunidad ?")
    tiempo = models.CharField(
        max_length=250, verbose_name="Tiempo involucrado/a en el Software Libre, ej 2 años")
    observaciones = models.TextField(
        verbose_name="¿Alguna observación adicional?")
    estado = models.SmallIntegerField(choices=ESTADOS, default=0)
    event = models.ForeignKey('EventECSL', on_delete=models.CASCADE, null=True, verbose_name=_("Event"))


    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Beca"
        verbose_name_plural = "Becas"


class EventECSL(models.Model):
    logo = models.ImageField(verbose_name=_("Logo"), null=True, upload_to='img/logos/',
                             blank=False)
    start_date = models.DateField(verbose_name=_("Start Date"), null=True)
    end_date = models.DateField(verbose_name=_("End Date"), null=True)
    location = models.CharField(max_length=50, null=True, verbose_name=_("Location"))
    description = models.TextField(verbose_name=_("Description"), null=True)
    current = models.BooleanField(default=False, verbose_name=_("Current"))
    organizer1 = models.CharField(max_length=25, null=True, verbose_name=_("First organizer"))
    organizer2 = models.CharField(max_length=25, null=True, verbose_name=_("Second organizer"))
    certificate_Header = models.ImageField(verbose_name=_("Certificate Header Image"), null=True, upload_to='img/logos/',
                             blank=True, help_text=_("Heigth 70px, Width 800px"))
    certificate_Footer = models.ImageField(verbose_name=_("Certificate Footer Image"), null=True, upload_to='img/logos/',
                             blank=True, help_text=_("Heigth 70px, Width 800px"))
    phone_event = models.CharField(max_length=15, null=True, verbose_name=_("Phone"))
    start_date_proposal = models.DateField(verbose_name=_("Start Date Proposal"), null=True)
    end_date_proposal = models.DateField(verbose_name=_("End Date Proposal"), null=True)
    email_event = models.CharField(max_length=50, null=True, verbose_name=_('Email Event'))

    @property
    def checking_period(self):
        current_date = timezone.localtime().date()
        if self.start_date_proposal <= current_date and current_date <= self.end_date_proposal:
            return True
        else:
            return False

    @property
    def checking_start_date(self):
        current_date = timezone.localtime().date()
        if self.start_date_proposal == current_date:
            return True
        else:
            return False

    def __str__(self):
        return _("Central American Free Software Meeting ") + str(self.start_date.year)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
