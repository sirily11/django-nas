import os
from time import time

import zipstream
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import webvtt

from nas.models import Folder, File, Logs
from nas.utils.utils import get_list_files, extra_text_from_current_files


@csrf_exempt
def download(request, folder):
    if request.method == "POST":
        return JsonResponse(
            data={"download_url": request.build_absolute_uri(reverse("download", kwargs={"folder": folder}))})
    """Download archive zip file of code snippets"""
    # response = HttpResponse(content_type='application/zip')

    folder = Folder.objects.get(id=folder)
    files = get_list_files(folder)

    z = zipstream.ZipFile(mode='w', allowZip64=True)
    for file in files:
        relative_filename = file.relative_filename(folder)
        z.write(file.file.path, relative_filename)

    response = StreamingHttpResponse(z, content_type='application/zip')
    zipfile_name = f"{folder.name}.zip"

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={zipfile_name}'
    return response


@csrf_exempt
def download_multiple_files(request):
    if request.method == "POST":
        import json
        json_data = json.loads(request.body)
        query = ""
        for i in json_data:
            query += f"files={i}&"
        url = request.build_absolute_uri(f"{reverse('download_multiple_files')}?{query[:-1]}")
        return JsonResponse(
            data={"download_url": url},
            status=201
        )

    files_index = request.GET.get("files")
    files = []
    if files_index is list:
        for i in files_index:
            files.append(File.objects.get(id=i))
    else:
        files.append(File.objects.get(id=files_index))
    z = zipstream.ZipFile(mode='w', allowZip64=True)
    for file in files:
        z.write(file.file.path, file.filename())

    response = StreamingHttpResponse(z, content_type='application/zip')
    zipfile_name = f"grouped_files.zip"

    # return as zipfile
    response['Content-Disposition'] = f'attachment; filename={zipfile_name}'
    return response


def convert_vtt_caption(request, file):
    from nas.utils.utils2 import WebVTTWriter
    f = File.objects.get(pk=file)
    vtt = webvtt.from_srt(f.file.path)
    captions = vtt.captions
    content = WebVTTWriter().write(captions)
    return JsonResponse(data={"content": content})


@csrf_exempt
def update_file_description(request):
    start_time = time()
    num = extra_text_from_current_files()
    end_time = time()
    content = "## Updated file description\n"
    content += f"Total time last: {end_time - start_time} seconds and had updated {num} files."
    Logs.objects.create(title="Updated file description", content=content, sender="System", log_type="UPDATED")
    return JsonResponse(data={"number_updates": num})


@csrf_exempt
def upload(request, file_index):
    from .key import aws_settings
    import boto3

    s3_client = boto3.client('s3', aws_access_key_id=aws_settings['access_id'],
                             aws_secret_access_key=aws_settings['access_key'])
    file = File.objects.filter(id=file_index).first()
    if file:
        try:
            p = file.parent
            path = os.path.basename(file.file.name)
            depth = 0
            while p:
                path = os.path.join(p.name, path)
                p = p.parent
                depth += 1
            if depth > 400:
                return JsonResponse(data={"message": "Too many folder"}, status=500)
            response = s3_client.upload_file(file.file.path, aws_settings['bucket_name'], path)
            file.has_uploaded_to_cloud = True
            file.save()
        except Exception as e:
            return JsonResponse(data={"message": str(e)}, status=500)
    else:
        return JsonResponse(status=404, data={"message": "file not found"})
    return JsonResponse(data={"status": "Ok"}, status=201)
