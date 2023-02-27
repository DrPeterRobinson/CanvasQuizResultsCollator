from datetime import date, datetime, timedelta
import yaml
import io
import markdown2
import requests
import os
import re

canvas_base_uri = "https://hull.instructure.com/api/v1";
# Hull access token
# regenerated 2/7/2019 (Overwatch)
canvas_access_token = "4738~V8bZONPsvtXh8izkaUBC7nd1Yz4ejTg7SXuBBYyKQLuwoYc1S9an97tsZgwhFn79";

upload_to_canvas=False

    canvas_course_id = yaml_data['canvas_course_id']
    canvas_assignment_id = yaml_data['canvas_assignment_id']

    # First, get list of image files from canvas (need to cross-refer to these)
    uri=f"https://hull.instructure.com/api/v1/courses/{canvas_course_id}/files?content_types[]=image&per_page=50"
    headers = {'Authorization':F'Bearer {canvas_access_token}'}
    response = requests.get(uri,headers=headers)
    data = response.json()