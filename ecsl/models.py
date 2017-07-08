from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class PaymentOption(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    identification = models.CharField(
        max_length=30, verbose_name=_('Identificación'), null=True)
    tipo = models.CharField(max_length=255, verbose_name=_('Opción de envío'))
    email = models.EmailField()

    def __str__(self):
        return "%s -- %s (%s)" % (self.tipo, self.name, self.identification)


class Gustos(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))

    def __str__(self):
        return self.name


class Encuentros_Anteriores(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))

    def __str__(self):
        return self.name


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
        ('Hondura', 'Honduras'),
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
        max_length=12, verbose_name=_('Identificación en su país'), null=True)
    born_date = models.DateField(
        verbose_name=_('Fecha de Nacimiento'), null=True)
    institution = models.CharField(
        max_length=12, null=True, blank=True, verbose_name=_('Institución'))
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

    @property
    def name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.user.get_full_name()


class Payment(models.Model):
    PAQUETE = (
        ('Completo', 'Completo (Habitación compartida en hostal - Alimentación - Ingreso a actividades)'),
        ('Sin hotel', 'Sin hotel (Acceso a actividades - Alimentación)'),

    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    option = models.ForeignKey(PaymentOption,
                               on_delete=models.CASCADE, verbose_name=_('Opción de pago'))
    codigo_de_referencia = models.CharField(max_length=40, verbose_name=_(
        'Id de transacción'), help_text="Identificación de transacción o código de referencia")
    paquete = models.CharField(max_length=40, choices=PAQUETE)
    invoice = models.FileField(upload_to="invoices/")
    confirmado = models.BooleanField(default=False)

    @property
    def opcion_paquete(self):
        return self.paquete

    @property
    def name(self):
        return self.user.get_full_name()

    def __str__(self):
        return "%s %s" % (self.user.get_full_name(), str(self.option))


class Patrocinadores(models.Model):
    class Meta:
        verbose_name_plural = 'Patrons'
        verbose_name = 'Patron'

    TYPES = (
        ('gold', 'Oro'),
        ('Plate', 'Plata'),
        ('Bronce', 'Bronce'),
    )
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    web = models.URLField(verbose_name=_('Web'))
    logo = models.ImageField(verbose_name=_('logo'), upload_to='logos/')
    patrocin = models.SmallIntegerField(choices=TYPES)


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

    def __str__(self):
        return self.user.get_full_name()
