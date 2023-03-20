# Generated by Django 4.0.8 on 2022-11-17 16:12

import django.db.models.deletion

from django.db import migrations, models
from django.contrib.contenttypes.models import ContentType

import logging

def moveSafi(apps, schema_editor):
    DeviceBGPSession = apps.get_model("netbox_cmdb", "DeviceBGPSession")
    AfiSafi = apps.get_model("netbox_cmdb", "AfiSafi")

    device_bgp_session_content_type = ContentType.objects.get_for_model(DeviceBGPSession)
    safis = AfiSafi.objects.all()

    for safi in safis:
        if safi.content_type_id == device_bgp_session_content_type.id:
            safi.device_bgp_session_id = safi.object_id
            safi.save()
        else:
            logging.warning("Not migrating SAFI for %s (most likely from a Peer Group)", safi.id)


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_cmdb', '0018_alter_bgppeergroup_remote_asn'),
    ]

    operations = [
        migrations.AddField(
            model_name='afisafi',
            name='device_bgp_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_out', to='netbox_cmdb.devicebgpsession'),
        ),
        migrations.RunPython(moveSafi),
    ]