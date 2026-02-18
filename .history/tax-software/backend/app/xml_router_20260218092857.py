"""
Expert XML Utilities for IRS/Tax/Workflow
- Parse, validate, and generate XML files
- Convert between JSON and XML
- Securely handle XML uploads/downloads
"""
import os
import xml.etree.ElementTree as ET
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import logging
from .auth_utils import bearer_auth, require_role
import json

router = APIRouter()
logger = logging.getLogger("tax-prep-app.xml")

XML_STORAGE = "xml_files/"
os.makedirs(XML_STORAGE, exist_ok=True)

def json_to_xml(json_obj, root_tag="Root"):
    root = ET.Element(root_tag)
    def build(elem, obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                child = ET.SubElement(elem, k)
                build(child, v)
        elif isinstance(obj, list):
            for v in obj:
                child = ET.SubElement(elem, "Item")
                build(child, v)
        else:
            elem.text = str(obj)
    build(root, json_obj)
    return ET.tostring(root, encoding="utf-8")

def xml_to_json(xml_str):
    root = ET.fromstring(xml_str)
    def parse(elem):
        children = list(elem)
        if not children:
            return elem.text
        result = {}
        for child in children:
            if child.tag not in result:
                result[child.tag] = parse(child)
            else:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(parse(child))
        return result
    return {root.tag: parse(root)}

@router.post("/xml/upload")
def upload_xml(file: UploadFile = File(...), user = Depends(require_role(["admin", "staff"]))):
    path = os.path.join(XML_STORAGE, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    logger.info(f"AUDIT: XML uploaded: {file.filename} by {user.email}")
    return {"message": "XML uploaded", "path": path}

@router.get("/xml/download")
def download_xml(filename: str, token: str = Depends(bearer_auth)):
    path = os.path.join(XML_STORAGE, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    logger.info(f"AUDIT: XML downloaded: {filename}")
    return FileResponse(path, media_type="application/xml")

@router.post("/xml/json-to-xml")
def api_json_to_xml(data: dict, token: str = Depends(bearer_auth)):
    xml_bytes = json_to_xml(data)
    logger.info("AUDIT: JSON to XML conversion performed")
    return {"xml": xml_bytes.decode()}

@router.post("/xml/xml-to-json")
def api_xml_to_json(xml: str, token: str = Depends(bearer_auth)):
    logger.info("AUDIT: XML to JSON conversion performed")
    return xml_to_json(xml)
