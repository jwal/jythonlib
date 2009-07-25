

import etree


def test():
    doc = etree.parse_string("""\
<fail type="epic">
  <site name="twitter" url="http://twitter.com"/>
</fail>
""")
    print [etree.tostring(r) for r in doc.xpath("//*")]
    print [r.attrib for r in doc.xpath("//*[@type]")]


if __name__ == "__main__":
    test()
