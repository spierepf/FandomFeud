from xml.etree import ElementTree as ET

from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))

from core.PygubuBuilder import GridLayoutManager, ObjectBuilder, InterfaceBuilder

if __name__ == '__main__':
    print('<?xml version=\'1.0\' encoding=\'utf-8\'?>')
    document = InterfaceBuilder().go()
    root = ET.SubElement(document, "object", {"class": "tk.Tk", "id": "root", "named": "True"})

    (
        ObjectBuilder(None, root, None)
        .add_property("height", 200)
        .add_property("width", 200)
        .add_frame()
        .add_frame("connect_frame", GridLayoutManager())
        .add_label("Host:")
        .add_entry("string:host_var", "127.0.0.1")
        .add_label("Port:")
        .add_entry("int:port_var", "8080")
        .add_button("Connect", "connect_to_server")
        .end_frame()
        .add_frame("round_frame")
        .add_frame("load_round_frame")
        .add_button("Begin Round", "begin_round")
        .end_frame()
        .add_frame("round_multiplier_frame", GridLayoutManager())
        .add_label("Round Multiplier")
        .add_radiobutton("Normal", "int:round_multiplier_var", 1)
        .add_radiobutton("Double", "int:round_multiplier_var", 2)
        .add_radiobutton("Triple", "int:round_multiplier_var", 3)
        .end_frame()
        .add_frame("score_frame", GridLayoutManager())
        .add_entry("int:left_score_var", "0", justify='center')
        .add_radiobutton("<<<", "string:event_var", "award_pot_to_left")
        .add_entry("int:pot_score_var", "0", justify='center')
        .add_radiobutton(">>>", "string:event_var", "award_pot_to_right")
        .add_entry("int:right_score_var", "0", justify='center')
        .end_frame()
        .add_frame("answers_frame").end_frame()
        .add_frame("strike_frame", GridLayoutManager())
        .add_radiobutton("Strike 1", "string:event_var", "strike_1")
        .add_radiobutton("Strike 2", "string:event_var", "strike_2")
        .add_radiobutton("Strike 3", "string:event_var", "strike_3")
        .end_frame()
        .add_frame("commit_frame")
        .add_button("Commit", "commit")
        .end_frame()
    )

    ET.indent(document, space="  ", level=0)
    ET.dump(document)
