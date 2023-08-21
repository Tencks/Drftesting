# Generated by Django 4.2.4 on 2023-08-21 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('technology', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Residente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreResidente', models.CharField(max_length=40)),
                ('apellidoResidente', models.CharField(max_length=40)),
                ('dniResidente', models.CharField(max_length=8, unique=True)),
                ('fechaNacimiento', models.DateField(default=None)),
                ('edad', models.IntegerField(default='Edad del residente')),
                ('genero', models.CharField(choices=[('0', 'Masculino'), ('1', 'Femenino'), ('2', 'No responder')], max_length=1)),
                ('medicoDeCabecera', models.CharField(max_length=40)),
                ('grupoSanguineo', models.CharField(default='Sangre', max_length=40)),
                ('numeroDeHabitacion', models.CharField(max_length=40)),
                ('observacionesResidente', models.TextField(default='SOME STRING')),
                ('localidadFamiliar', models.CharField(default='Localidad', max_length=60)),
                ('domicilioFamiliar', models.CharField(default='Domicilio', max_length=60)),
                ('nombreFamiliar', models.CharField(max_length=40)),
                ('apellidoFamiliar', models.CharField(max_length=40)),
                ('numeroTelefonico', models.CharField(max_length=40)),
                ('dniFamiliar', models.CharField(default='Dni familiar', max_length=8, unique=True)),
                ('numeroAfiliado', models.IntegerField(unique=True)),
                ('obraSocial', models.CharField(max_length=40)),
                ('vinculoConElResidente', models.CharField(choices=[('0', 'Padre'), ('1', 'Madre'), ('2', 'Hijo'), ('3', 'Hija'), ('4', 'Abuelo'), ('5', 'Abuela'), ('6', 'Tío'), ('7', 'Tía'), ('8', 'Pariente lejano'), ('9', 'Prefiero no responder')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='StockMedicamentosLocal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genericMedicamento', models.CharField(choices=[('Y', 'Si'), ('N', 'No')], max_length=1)),
                ('nombreMedicamento', models.CharField(max_length=80)),
                ('marcaMedicamento', models.CharField(max_length=60)),
                ('pesoMedicamento', models.CharField(max_length=35)),
                ('cantDisponible', models.IntegerField()),
                ('medicionMedicamento', models.CharField(choices=[('0', 'ml'), ('1', 'g'), ('2', 'píldora/as'), ('3', 'caja/as'), ('4', 'frasco/os')], max_length=1)),
                ('fechaIngreso', models.DateField(default=None)),
                ('fechaCaducidad', models.DateField(default=None)),
                ('codMedicamento', models.CharField(max_length=50)),
                ('observacionesMedicamento', models.TextField(default='SOME STRING')),
                ('derivacionesMedicamento', models.TextField(default='SOME STRING')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('cargo', models.CharField(choices=[('0', 'invitado'), ('1', 'Medico/a'), ('2', 'Enfermero/a'), ('3', 'Empleado diario'), ('4', 'Admin')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='StockMedicamentosResidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genericMedicamento', models.CharField(choices=[('Y', 'Si'), ('N', 'No')], max_length=1)),
                ('nombreMedicamento', models.CharField(max_length=80)),
                ('marcaMedicamento', models.CharField(max_length=60)),
                ('pesoMedicamento', models.CharField(max_length=35)),
                ('cantDisponible', models.IntegerField()),
                ('medicionMedicamento', models.CharField(choices=[('0', 'ml'), ('1', 'g'), ('2', 'píldora/as'), ('3', 'caja/as'), ('4', 'frasco/os')], max_length=1)),
                ('fechaIngreso', models.DateField(default=None)),
                ('fechaCaducidad', models.DateField(default=None)),
                ('codMedicamento', models.CharField(max_length=50)),
                ('observacionesMedicamento', models.TextField(default='SOME STRING')),
                ('derivacionesMedicamento', models.TextField(default='SOME STRING')),
                ('residenteM', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicamentos', to='quickstart.residente')),
            ],
        ),
        migrations.CreateModel(
            name='ObservaciónSemanal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaConsulta', models.DateField(auto_now_add=True)),
                ('tensionArterial', models.CharField(max_length=20)),
                ('glucemia', models.CharField(max_length=20)),
                ('saturacion', models.CharField(max_length=20)),
                ('pulso', models.CharField(max_length=30)),
                ('observacionesSemanales', models.TextField(default='some string')),
                ('derivacionesSemanales', models.TextField(default='some string2')),
                ('residenteS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signosVitales', to='quickstart.residente')),
            ],
        ),
    ]
