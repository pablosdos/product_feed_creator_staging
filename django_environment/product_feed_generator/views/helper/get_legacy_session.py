"""
find
out
in_stock
of ingram micro product
"""
import requests
import urllib3
import ssl
import xmltodict

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

def get_availability(ingram_part_number_for_xml_request):
    site = "https://mercury.ingrammicro.com/SeeburgerHTTP/HTTPController?HTTPInterface=syncReply"
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <BusinessTransactionRequest xmlns="http://www.ingrammicro.com/pcg/in/PriceAndAvailibilityRequest">
        <RequestPreamble>
            <SenderID>123456789010</SenderID>
            <ReceiverID>8712423012622</ReceiverID>
            <TransactionClassifier>2.0</TransactionClassifier>
            <TransactionID>Example PriceAvailability</TransactionID>
            <TimeStamp>2018-11-30T11:57:39</TimeStamp>
            <UserName>NL_363384XM</UserName>
            <UserPassword>sUFakI5a@</UserPassword>
            <CountryCode>NL</CountryCode>
        </RequestPreamble>
        <PriceAndAvailabilityRequest>
            <PriceAndAvailabilityPreference>3</PriceAndAvailabilityPreference>
            <CurrencyCode>EUR</CurrencyCode>
            <Item>
                <!-- IngramPartNumber | VendorPartNumber -->
                <IngramPartNumber>%s</IngramPartNumber>
                <RequestedQuantity UnitOfMeasure="EA">1</RequestedQuantity>
                <ReserveInventorySearchFlag>Y</ReserveInventorySearchFlag>
            </Item>
        </PriceAndAvailabilityRequest>
    </BusinessTransactionRequest>
    """ % ingram_part_number_for_xml_request
    headers = {"Content-Type": "application/xml"}
    params = {'sessionKey': 'syncReply'}
    # print(get_legacy_session().get(site, data=xml).text)
    xml_data = xmltodict.parse(get_legacy_session().get(site, data=xml).text)
    """
    TODO – IMPLEMENT 
    MORE LOCATIONS OF THE QUANTITY
    """
    try:
        return xml_data["BusinessTransactionResponse"]["PriceAndAvailabilityResponse"]["ItemDetails"]["AvailabilityDetails"]["Plant"]["AvailableQuantity"]['#text']
    except:
        return 'unknown'