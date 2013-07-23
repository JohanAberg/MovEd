import re
import xml.dom.minidom as xml

class Xml(object):

    def __init__(self):
        self.file_name = '/tmp/mlt_tractor.xml'

    def create_xml(self):

        #### PROJECT XML ####
        # Create the XML document
        dom = xml.Document()

        # Add the root element
        xml_root = dom.createElement("mlt")
        dom.appendChild(xml_root)
        tractor1 = dom.createElement("tractor")
        tractor1.setAttribute("id", "tractor0")
        xml_root.appendChild(tractor1)

        #### SEQUENCE XML ####
        multitrack = dom.createElement("multitrack")
        tractor1.appendChild(multitrack)

        #### TRACK XML ####
        playlist = dom.createElement("playlist")
        playlist.setAttribute("id", 'no_Name')
        multitrack.appendChild(playlist)

        #### CLIP XML ####

        # determine length of this clip
        ending_frame = 1000

        # create the clip producer node
        producer = dom.createElement("producer")
        producer.setAttribute("id", '123456')
        producer.setAttribute("novdpau", "1")
        producer.setAttribute("in", str(int(round(0))))
        producer.setAttribute("out", str(int(round(1000))))
        producer.setAttribute("length", str(int(round(1000) + 1)))

        # add the RESOURCE to the producer node
        property = dom.createElement("property")
        property.setAttribute("name", "resource")
        text = dom.createTextNode('/home/aberg/Downloads/sample_iTunes.mov')
        property.appendChild(text)
        producer.appendChild(property)

        # add producer
        playlist.appendChild(producer)


        # Pretty print using a Regular expression (I am using regex due to a bug in the minidom, with extra
        # whitespace in it's pretty print method.  This should fix the pretty print's white space issue.)
        pretty_print = re.compile(r'((?<=>)(\n[\t]*)(?=[^<\t]))|((?<=[^>\t])(\n[\t]*)(?=<))')
        pretty_print_output = re.sub(pretty_print, '', dom.toprettyxml())

        # Save the XML dom
        f = open(self.file_name, "w")
        f.write(pretty_print_output)
        f.close()


if __name__ == '__main__':

    x = Xml()
    x.create_xml()