import easyocr
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

reader = easyocr.Reader(['ko'])
