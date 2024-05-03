import pandas as pd
from gspread import *
from datetime import datetime
from lxml import etree
from xhtml2pdf import pisa

#from utils.xslt import transform_xml

# CONST 
REP_FILE_NAME = 'Data Model - Gestionale Spazio Exe'
DEVICES_FILE_NAME = ''
ACC_FILE_NAME = ''
CASSA_FILE_NAME = 'Cassa'
XML_SOURCE = 'temp_source.xml'
XML_SOURCE = "data/temp_source.xml"  # Path to the input XML file
HTML_DEST = "data/temp_receipt.html"  # Path where the output HTML will be saved
XSLT_PATH = "utils/XmlToHtml.xslt"


# Data 
def get_data(worksheet : Worksheet):
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def xml_writer(input_data:dict, item_type:str):


    price = str(input_data["price"])
    

    with open(XML_SOURCE, "w", encoding="utf-8") as f : 
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<items>\n")

    with open(XML_SOURCE, "a", encoding="utf-8") as f : 
        f.write("<item>\n"+
                "<type>"+item_type+"</type>\n"+
                "<first_name>"+input_data["first_name"]+"</first_name>\n"+
                "<last_name>"+input_data["last_name"]+"</last_name>\n"+
                "<request_date>"+datetime.now().strftime("%Y-%m-%d")+"</request_date>\n"+
                "<last_date>"+datetime.now().strftime("%Y-%m-%d")+"</last_date>\n"+
                #"<price>"+price+"</price>\n"+     
                "<device>"+input_data["device"]+"</device>\n"+
                "<brand>"+input_data["brand"]+"</brand>\n"+
                "<model>"+input_data["model"]+"</model>\n"+
                "<state>"+input_data["state"]+"</state>\n"+
                "<operator>"+input_data["operator"]+"</operator>\n"+
                "<left_accessory>"+input_data["left_accessory"]+"</left_accessory>\n"+
                "<unlock_code>"+input_data["unlock_code"]+"</unlock_code>\n"+
                "<color>"+input_data["color"]+"</color>\n"+
                "<action>"+input_data["action"]+"</action>\n"+
                "<url>"+input_data["url"]+"</url>\n"+
                "<muletto>"+input_data["muletto"]+"</muletto>\n")

    with open(XML_SOURCE, "a",  encoding="utf-8") as f : 
        f.write("</item>\n</items>\n")


# XSLT Transformer
def load_xml(xml_path: str):
    """ Load an XML file from the specified path. """
    with open(xml_path, 'rb') as file:
        return etree.XML(file.read())

def transform_xml(xml_path: str, html_path: str):
    """ Transform the specified XML file into HTML using the XSLT file and save to html_path. """
    xml = load_xml(xml_path)
    xslt = etree.parse(XSLT_PATH)
    transform = etree.XSLT(xslt)
    result = transform(xml)
    
    # Write the result to an HTML file
    with open(html_path, 'wb') as f:
        f.write(etree.tostring(result, pretty_print=True))

# PDF Generator
def convert_html_to_pdf(source_html, output_filename):
    # Utility function to convert HTML to PDF
    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(
        source_html,                # the HTML to convert
        dest=result_file)           # file handle to receive result
    result_file.close()            # close output file
    return pisa_status.err         # return True on success

def gen_recap(input_fields:dict, file_download_name:str="output.pdf"):

    xml_writer(input_fields,"Riparazioni")
    transform_xml(XML_SOURCE, HTML_DEST)

    with open(HTML_DEST, 'r') as file:
        html_content = file.read()

    convert_html_to_pdf(html_content, 'data/'+file_download_name) 

    return file_download_name
