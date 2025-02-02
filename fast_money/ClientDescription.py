from xml.etree import ElementTree as ET

from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))

from core.PygubuBuilder import GridLayoutManager, ObjectBuilder, InterfaceBuilder

if __name__ == '__main__':
    print('<?xml version=\'1.0\' encoding=\'utf-8\'?>')
    document = InterfaceBuilder().go()
    root = ET.SubElement(document, "object", {"class": "tk.Tk", "id": "root", "named": "True"})

    tmp = (
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
        .add_frame("timer_frame", GridLayoutManager())
        .add_label("Duration")
        .add_entry("int:duration_entry_var", 20)
        .add_button("Set", "set_timer_duration")
        .add_button("Start", "start_timer")
        .add_button("Duplicate", "play_duplicate_sound")
        .end_frame()
        .add_frame("answer_frame", GridLayoutManager())
    )
    for col in range(2):
        tmp = tmp.add_frame(None, GridLayoutManager())
        for row in range(5):
            tmp = (
                tmp
                .add_entry(f"string:answer_{col*5+row}_entry_var", " ")
                .add_radiobutton("", "string:event_var", f"reveal_answer_{col*5+row}")
                .add_entry(f"int:score_{col*5+row}_entry_var", 0, width=3)
                .add_radiobutton("", "string:event_var", f"reveal_score_{col*5+row}")
                .next_row())
        tmp = tmp.end_frame()
    (
        tmp
        .end_frame()
        .add_frame("commit_frame")
        .add_button("Commit", "commit")
        .end_frame()
    )

    ET.indent(document, space="  ", level=0)
    ET.dump(document)
