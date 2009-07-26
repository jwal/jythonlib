

import etree


def test():
    doc = etree.parse_string("""\
<fail type="epic">
  <site name="twitter" url="http://twitter.com"/>
</fail>
""")
    print [etree.tostring(r) for r in doc.xpath("//*")]
    print [r.attrib for r in doc.xpath("//*[@type]")]
    doc = etree.parse_string("""\
<t:pass layout="pretty" xml:lang="en" s:style="really-pretty"
        xmlns:t="testing.example.com" xmlns:s="style.example.com"
        xmlns="books.example.com">
  <book name="War and Peace" author="Leo Tolstoy"/>
</t:pass>
""")
    print [r.tag for r in 
           doc.xpath("//b:book[@author=$author]", 
                     namespaces={"b": "books.example.com"},
                     author="Leo Tolstoy")]
    print [r.attrib for r in 
           doc.xpath("//t:*", namespaces={"t": "testing.example.com"})]


if __name__ == "__main__":
    test()
