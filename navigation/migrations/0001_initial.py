# Generated by Django 4.2.9 on 2024-12-14 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('distance_sum', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=255)),
                ('city_eng', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_eng', models.CharField(max_length=255)),
                ('deans_office_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('description_eng', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('name_eng', models.CharField(max_length=255)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('description_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objects', to='navigation.address')),
                ('guide', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objects', to='navigation.guide')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'unique_together': {('latitude', 'longitude')},
            },
        ),
        migrations.CreateModel(
            name='AreaObject',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='navigation.object')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('is_paid', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('navigation.object',),
        ),
        migrations.CreateModel(
            name='PointObject',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='navigation.object')),
                ('event_category', models.CharField(blank=True, max_length=255, null=True)),
                ('event_start', models.DateTimeField(blank=True, null=True)),
                ('event_end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('navigation.object',),
        ),
        migrations.CreateModel(
            name='UserObjectSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('route_created_count', models.IntegerField()),
                ('object_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_object_search', to='navigation.object')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_object_search', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_eng', models.CharField(max_length=255)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute', to='navigation.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='ImportantPlace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('floor', models.IntegerField()),
                ('room', models.CharField(blank=True, max_length=255, null=True)),
                ('object_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='important_place', to='navigation.object')),
            ],
        ),
        migrations.CreateModel(
            name='AreaObjectFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(blank=True, max_length=255, null=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_associations', to='navigation.faculty')),
                ('object_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_associations', to='navigation.areaobject')),
            ],
        ),
        migrations.AddField(
            model_name='faculty',
            name='area_objects',
            field=models.ManyToManyField(related_name='faculties', through='navigation.AreaObjectFaculty', to='navigation.areaobject'),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('object_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry', to='navigation.object')),
            ],
            options={
                'unique_together': {('latitude', 'longitude')},
            },
        ),
    ]