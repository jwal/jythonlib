
# An implementation of part of the API provided by the lxml.etree
# library for xpython but suitable for use with Jython 2.5 on J2SE6.

from org.dom4j import DocumentHelper
from org.dom4j import Namespace
from org.dom4j import QName
from org.dom4j.io import SAXReader
from org.jaxen import SimpleVariableContext;
from org.jaxen import VariableContext;


def _format_qname(qname):
    if qname.namespaceURI == "":
        return qname.name
    else:
        return "{%s}%s" % (qname.namespaceURI, qname.name)


def _make_qname(long_name):
    if "}" in long_name:
        namespace, name = long_name.lstrip("{").split("}")
        return QName(name, Namespace(None, namespace))
    else:
        return QName(long_name, Namespace.NO_NAMESPACE)


class RootTree(object):

    def __init__(self, doc):
        self._doc = doc

    def xpath(self, *args, **kwargs):
        return self.getdocumentelement().xpath(*args, **kwargs)

    def getdocumentelement(self):
        return Element(self._doc.getRootElement())


class Attributes(object):

    def __init__(self, elem):
        self._elem = elem

    def iteritems(self):
        return ((_format_qname(a.getQName()), a.value) for a 
                in self._elem.attributeIterator())

    def items(self):
        return list(self.iteritems())

    def __setitem__(self, key, value):
        self._elem.setAttributeValue(_make_qname(key), value)

    def __getitem__(self, key):
        return dict(self.iteritems())[key]

    def __delitem__(self, key): 
        # Check for key error
        dict(self.iteritems())[key]
        self._elem.setAttributeValue(_make_qname(key), None)

    def get(self, key, default=None):
        return dict(self.iteritems()).get(key, default)

    def __repr__(self):
        return "<%s {%s}>" % (type(self).__name__,
                              ", ".join("%r: %r" % (k, v) for (k, v) 
                                        in sorted(self.items())))


class BrokenVariableContext(VariableContext):

    # I don't understand namespaces for xpath variables, until I do
    # I'll pretend they don't exist.

    def __init__(self, values):
        self._values = values

    def getVariableValue(self, namespace, prefix, name):
        return self._values[name]


class Element(object):

    def __init__(self, elem):
        self._elem = elem

    def xpath(self, query, namespaces=(), **kwargs):
        variables = BrokenVariableContext(kwargs)
        xpathSelector = DocumentHelper.createXPath(query)
        xpathSelector.setNamespaceURIs(dict(namespaces))
        xpathSelector.setVariableContext(variables)
        return [Element(e) for e in xpathSelector.selectNodes(self._elem)]

    @property
    def attrib(self):
        return Attributes(self._elem)

    @property
    def tag(self):
        return _format_qname(self._elem.getQName())

    
def parse_file(filename):
    # Untested so far
    return RootTree(SAXReader().read(filename))


def parse_string(text):
    return RootTree(DocumentHelper.parseText(text))


def tostring(element):
    return element._elem.asXML()
