#coding=utf-8
from CTFd.utils.user import is_admin, get_current_user
from CTFd.models import Users
from CTFd.utils.countries import lookup_country_code
from six.moves.urllib.parse import urlparse, urljoin
from flask import request
from marshmallow import ValidationError
import re


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def validate_url(url):
    return urlparse(url).scheme.startswith("http")


def validate_email(email):
    return bool(re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))


def unique_email(email, model=Users):
    obj = model.query.filter_by(email=email).first()
    if is_admin():
        if obj:
            raise ValidationError("Email address has already been used")
    if obj and obj.id != get_current_user().id:
        raise ValidationError("Email address has already been used")


def validate_country_code(country_code):
    if country_code.strip() == "":
        return
    if lookup_country_code(country_code) is None:
        raise ValidationError("Invalid Country")


def unique_website(website, model=Users):
    if website is None:
        return
    if re.match(r"^\d{10}$", website) is None:
        raise ValidationError("学号格式不正确")
    obj = model.query.filter_by(website=website).first()
    if is_admin():
        if obj:
            raise ValidationError("学号已被使用")
    if obj and obj.id != get_current_user().id:
        raise ValidationError("学号已被使用")


def unique_affiliation(affiliation, model=Users):
    obj = model.query.filter_by(affiliation=affiliation).first()
    if is_admin():
        if obj:
            raise ValidationError("姓名已被使用")
    if obj and obj.id != get_current_user().id:
        raise ValidationError("姓名已被使用")
