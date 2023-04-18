from tenable.io import TenableIO
from .dradis import Dradis
import os
from dotenv import load_dotenv


load_dotenv()

accesskey = os.getenv('TENABLE_ACCESS_KEY')
secretkey = os.getenv('TENABLE_SECRET_KEY')
api_token = os.getenv('DRADIS_API_KEY')
url = 'https://cofc-dradis.soteria.io'

tio = TenableIO(accesskey, secretkey)
dradis_api = Dradis(api_token, url)
