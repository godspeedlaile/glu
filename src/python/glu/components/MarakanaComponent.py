"""
A component that can accept POST messages for new orders
from Marakana.

"""
# Python imports
import time
import glujson as json
import StringIO
import xml.etree.ElementTree as ET

# Glu imports
from glu.components.api import *

class MarakanaComponent(BaseComponent):
    NAME             = "MarakanaComponent"
    
    PARAM_DEFINITION = {
                           "salesforce_resource" : ParameterDef(PARAM_STRING, "URL of our salesforce resource", required=True)
                       }

    DESCRIPTION      = "Allows the storage of new orders that are POSTed by Marakana."
    DOCUMENTATION    =  """
                        This component is used to store objects that are pushed to us by Marakana.

                        A brief sanity check is performed.

                        """
    SERVICES         = {
                           "orders" :   {
                               "desc"   : "Accepts POSTed new orders and allows the browsing and retrieval of existing orders.",
                               "params" : {
                                    "id" : ParameterDef(PARAM_STRING, "Order id", required=False, default=""),
                               },
                               "positional_params" : [ "id" ]
                           },
                           "matches" :   {
                               "desc"   : "Calculates the matches between order data and salesforce data.",
                           }
                        }

    #
    # Template for the product order dictionary.
    # Our sanity checking compares what we received to this dictionary,
    # to ensure that at least the items listed here are present in the
    # received dictionary. The type of an item is either a dictionary,
    # list or other basic type, such as string. For string we specify
    # "str" (which is a string), while for boolean, we would just set
    # True or False, for a number 123, etc.
    #
    __PRODUCT_ORDER_TEMPLATE = {
        "spark-domain" : {
            "product-order" : {
                "__attributes" : {
                    "id" : "str"
                },
                "customer" : {
                    "first-name"   : "str",
                    "last-name"    : "str",
                    "title"        : "str",
                    "office-phone" : "str",
                    "email"        : "str",
                    "address" : {
                        "street1"      : "str",
                        "city"         : "str",
                        "region"       : "str",
                        "postal-code"  : "str",
                        "country"      : "str",
                    },
                },
                "customer-organization-ref" : "str",
                "taxable-subtotal" : "str",
                "product-item" : {
                    "product-ref" : "str",
                },
            }
        }
    }

    __REGISTRATION_ORDER_TEMPLATE = {
        "spark-domain" : {
            "registration-order" : {
                "__attributes" : {
                    "id" : "str"
                },
                "customer" : {
                    "first-name"   : "str",
                    "last-name"    : "str",
                    "title"        : "str",
                    "office-phone" : "str",
                    "email"        : "str",
                    "address" : {
                        "street1"      : "str",
                        "city"         : "str",
                        "region"       : "str",
                        "postal-code"  : "str",
                        "country"      : "str",
                    },
                },
                "customer-organization-ref" : "str",
                "taxable-subtotal" : "str",
                "registration" : [],
            }
        }
    }
    
    def __get_order_list(self, storage):
        """
        Helper function that returns a list of URIs for stored orders.

        """
        # User didn't specify a specific order (and also doesn't POST a new order object),
        # which means we should generate a list of all the orders we have stored.
        data = storage.listFiles()

        # We want to prepend the resource name and service name, so that the user
        # gets complete URIs for each file
        my_resource_uri = self.getMyResourceUri()
        new_data = [ "%s/%s/%s" % (my_resource_uri, "orders", name) for name in data ]
        return new_data

    def __xml_to_dict_process(self, el):
        """
        This converts some XML to a Python dictionary. Seems to do a pretty good
        job at it as well.

        It's dense and nasty code, I know...

        Started out with this code here:

            http://stackoverflow.com/questions/127606/editing-xml-as-a-dictionary-in-python/2303733#2303733

        I added handling of attributes and lists.

        """
        d={}
        tag = el.tag
        #
        # If the document specifies a domain then element tree will list the domain URL as a prefix
        # for every single tag. That's extremely annoying. The format is "{http://...}foobar". Therefore,
        # I keep looking for '}' and stip away everything before.
        #
        i = tag.find("}")
        tag = tag[i+1:]
        if el.text:
            d[tag] = el.text
        else:
            d[tag] = {}
        children = el.getchildren()
        if children:
            d[tag] = {}
            for child in children:
                child_tag = child.tag[child.tag.find("}")+1:]
                if child_tag in d[tag]:
                    if type(d[tag][child_tag]) is list:
                        d[tag][child_tag].append(self.__xml_to_dict_process(child)[child_tag])
                    else:
                        if type(d[tag][child_tag]) is dict  and  child_tag in d[tag][child_tag]:
                            old_elem = d[tag][child_tag][child_tag]
                        else:
                            old_elem = d[tag][child_tag]
                        d[tag][child_tag] = [ old_elem, self.__xml_to_dict_process(child)[child_tag] ]
                else:
                    child_out = self.__xml_to_dict_process(child)
                    if type(child_out) is dict:
                        child_out = child_out[child_tag]
                    d[tag][child_tag] = child_out
            if el.attrib:
                d[tag]['__attributes'] = el.attrib
        return d

    def __xml_to_dict(self, buf):
        """
        Helper method that translates XML to a dictionary.

        Attributes are appended as special parameters in the list.

        This just starts the recursive process method after
        initializing the element tree parsing and finding the
        root element.

        """
        f   = StringIO.StringIO(buf.strip())
        doc = ET.parse(f)
        el  = doc.getroot()
        return self.__xml_to_dict_process(el)

    def __dict_struct_compare(self, is_dict, should_dict):
        """
        Compare the structure of two dictionaries.

        The 'should_dict' contains elements and types. The method checks
        whether the 'is_dict' contains the same elements and types.

        """
        for key, item in should_dict.items():
            if key not in is_dict:
                raise Exception("Missing key '%s'" % key)
            if type(item) is not type(is_dict[key]):
                raise Exception("Type mismatch for key '%s'. Is '%s', should be '%s'" % (key, type(is_dict[key]), type(item)))
            if type(item) is dict:
                self.__dict_struct_compare(is_dict[key], item)

    def orders(self, method, input, id):
        """
        Stored or retrieves data from the storage bucket for Marakana orders.
        
        @param method:     The HTTP request method.
        @type method:      string
        
        @param input:      Any data that came in the body of the request.
        @type input:       string
        
        @return:           The output data of this service.
        @rtype:            string
        
        """
        # Access to our storage bucket
        storage   = self.getFileStorage()

        # Get my parameters
        param_order_id = id
        if not param_order_id  and  not input:
            # User didn't specify a specific order (and also doesn't POST a new order object),
            # which means we should generate a list of all the orders we have stored.
            return Result.ok(self.__get_order_list(storage))
        else:
            if method == HTTP.DELETE:
                if param_order_id:
                    storage.deleteFile(param_order_id)
                    return Result.ok("File deleted")
                else:
                    return Result.badRequest("Missing order id")
            else:
                if input:
                    # Parse the input into JSON
                    d = self.__xml_to_dict(input)
                    # Sanity check
                    try:
                        if 'product-order' in d['spark-domain']:
                            is_product_order = True
                            doc_name         = 'product-order'
                            self.__dict_struct_compare(d, self.__PRODUCT_ORDER_TEMPLATE)
                            order_id = d['spark-domain']['product-order']['__attributes']['id']
                        else:
                            is_product_order = False
                            doc_name         = 'registration-order'
                            self.__dict_struct_compare(d, self.__REGISTRATION_ORDER_TEMPLATE)
                            order_id = d['spark-domain']['registration-order']['__attributes']['id']
                    except Exception, e:
                        return Result.badRequest("Malformed request  body: " + str(e))
                    
                    # Creating or updating order
                    location_str = "%s/orders/%s" % (self.getMyResourceUri(), order_id)
                    if param_order_id:
                        if param_order_id != order_id:
                            return Result.badRequest("Order ID in URL and message body do not match (%s vs. %s)" % (param_order_id, order_id))
                        # Update an already existing order? Throws exception if it does not
                        # exist, which is exactly what we want.
                        dummy_data = storage.loadFile(order_id)
                        result = Result.ok("Successfully updated: %s" % location_str)
                    else:
                        # Creating a new order? We need to extract the order id.
                        result = Result.created(location_str, "Successfully stored: %s" % location_str)

                    # Store the data, but only the dictionary that contains the actual order info.
                    # We store it in a dictionary that contains a single key and this data, since
                    # that makes it look ... nice.
                    storage.storeFile(order_id, json.dumps({ doc_name : d['spark-domain'][doc_name] }))
                else:
                    # Just want to retrieve an existing order
                    result = Result.ok(json.loads(storage.loadFile(param_order_id)))

        return result


    def matches(self, method, input):
        storage    = self.getFileStorage()
        order_list = storage.listFiles()

        salesforce_resource_uri = self.salesforce_resource

        match_count = 0
        out         = dict()
        for order_id in order_list:
            order = json.loads(storage.loadFile(order_id))
            #
            # The ID and customer field are at the same location in both
            # types of orders. There is only one element in the top-level
            # dictionary, so we can say:
            top_level_key = order.keys()[0]
            d = order[top_level_key]
            customer_email = d['customer']['email']
            print "customer email: ", customer_email
            print "salesforce URI: ", salesforce_resource_uri
            code, matches = accessResource('%s/contact/data/email/"%s"' % (salesforce_resource_uri, customer_email))
            if code != HTTP.OK:
                raise GluException("Error accessing Salesforce resource: " + str(matches))
            print matches
            if top_level_key == 'product-order':
                prod_name = d['product-item']['product-ref']
                prod_type = "product"
            else:
                prod_name = d['registration'][0]['course-event-ref']['course-ref']
                prod_type = "registration"
            keystr = "%s, %s (%s) of %s ordered training %s '%s' for $%s" % (d['customer']['last-name'], d['customer']['first-name'], \
                                                                 d['customer']['email'], d['customer-organization-ref'], \
                                                                 prod_type, prod_name, d['taxable-subtotal'])
            if matches:
                match_count += len(matches)
                desc = dict()
                mo = list()
                for m in matches:
                    td = dict()
                    td[' Name']                = m['Name']
                    td['Address 1: Street']    = m['MailingStreet']
                    td['Address 2: City']      = m['MailingCity']
                    td['Address 3: State']     = m['MailingState']
                    td['Address 4: Country']   = m['MailingCountry']
                    td['CLICK HERE TO UPDATE SALESFORCE'] = self.getMyResourceUri() + "/integrate/" + order_id + "/" + m['Id']
                    mo.append(td)
                    
                order_data = { keystr : mo }
            else:
                order_data = { keystr : None }

            out[order_id] = order_data


        out['summary'] = "%d matches." % match_count
        return Result.ok(out)


