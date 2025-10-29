from xml.etree import ElementTree as ET


class IdGenerator:
    def __init__(self):
        self.next_id = 0

    def id(self):
        retval = f'object_{self.next_id}'
        self.next_id += 1
        return retval


class PackLayoutManager:
    def layout(self, object):
        layout = ET.SubElement(object, "layout", {'manager': 'pack'})
        ET.SubElement(layout, "property", {"name": "side"}).text = "top"

    def next_row(self):
        pass


class GridLayoutManager:
    def __init__(self):
        self.col = 0
        self.row = 0

    def layout(self, object):
        layout = ET.SubElement(object, "layout", {'manager': 'grid'})
        ET.SubElement(layout, "property", {"name": "column"}).text = str(self.col)
        ET.SubElement(layout, "property", {"name": "row"}).text = str(self.row)
        self.col += 1

    def next_row(self):
        self.col = 0
        self.row += 1


class ObjectBuilder:
    def __init__(self, parent_builder, root, id_generator):
        self.parent_builder = parent_builder
        self.root = root
        self.id_generator = id_generator if id_generator else IdGenerator()
        self.layout_manager = PackLayoutManager()

    def layout(self, object):
        self.layout_manager.layout(object)

    def add_property(self, name, value):
        ET.SubElement(self.root, "property", {"name": name}).text = str(value)
        return self

    def initialize_object(self, clazz, object_id):
        child = ET.SubElement(self.root, "child")
        attrib = {"class": clazz}
        if object_id:
            attrib["id"] = object_id
            attrib["named"] = "True"
        else:
            attrib["id"] = self.id_generator.id()
        object = ET.SubElement(child, "object", attrib)
        return object

    def add_frame(self, object_id=None, layout_manager=PackLayoutManager()):
        object = self.initialize_object("ttk.Frame", object_id)
        ET.SubElement(object, "property", {"name": "height"}).text = str(200)
        ET.SubElement(object, "property", {"name": "width"}).text = str(200)
        self.layout(object)
        return FrameBuilder(self, object, self.id_generator, layout_manager)

    def add_label(self, text, object_id=None):
        object = self.initialize_object("ttk.Label", object_id)
        ET.SubElement(object, "property", {"name": "style"}).text = "primary.TLabel"
        ET.SubElement(object, "property", {"name": "text", "translatable": "yes"}).text = str(text)
        self.layout(object)
        return self

    def add_entry(self, variable, text, justify=None, width=None, object_id=None):
        object = self.initialize_object("ttk.Entry", object_id)
        ET.SubElement(object, "property", {"name": "font"}).text = "{Liberation Sans} 24 {}"
        if justify:
            ET.SubElement(object, "property", {"name": "justify"}).text = str(justify)
        ET.SubElement(object, "property", {"name": "text", "translatable": "yes"}).text = str(text)
        ET.SubElement(object, "property", {"name": "textvariable"}).text = str(variable)
        if width:
            ET.SubElement(object, "property", {"name": "width"}).text = str(width)
        self.layout(object)
        return self

    def add_button(self, text, command, object_id=None):
        object = self.initialize_object("ttk.Button", object_id)
        ET.SubElement(object, "property", {"name": "command", "type": "command", "cbtype": "simple"}).text = str(command)
        ET.SubElement(object, "property", {"name": "style"}).text = "primary.TButton"
        ET.SubElement(object, "property", {"name": "text", "translatable": "yes"}).text = str(text)
        self.layout(object)
        return self

    def add_radiobutton(self, text, variable, value, object_id=None):
        object = self.initialize_object("ttk.Radiobutton", object_id)
        ET.SubElement(object, "property", {"name": "text", "translatable": "yes"}).text = str(text)
        ET.SubElement(object, "property", {"name": "style"}).text = "primary.TRadiobutton"
        ET.SubElement(object, "property", {"name": "value"}).text = str(value)
        ET.SubElement(object, "property", {"name": "variable"}).text = str(variable)
        self.layout(object)
        return self

    def next_row(self):
        if self.layout_manager:
            self.layout_manager.next_row()
        return self

    def end_frame(self):
        return self.parent_builder


class FrameBuilder(ObjectBuilder):
    def __init__(self, parent_builder, parent_document, id_generator, layout_manager):
        super().__init__(parent_builder, parent_document, id_generator)
        self.layout_manager = layout_manager


class InterfaceBuilder:
    def __init__(self):
        self.project_name = "Client"
        self.project_description = "A tkinter client."
        self.module_name = "client"
        self.main_classname = "Client"
        self.next_id = 0

    def go(self):
        document = ET.Element("interface", {"version": "1.4", "author": "PygubuDesigner 0.41.4"})
        project = ET.SubElement(document, "project")
        settings = ET.SubElement(project, "settings")

        for k, v in {
            "name": self.project_name,
            "description": self.project_description,
            "module_name": self.module_name,
            "template": "application",
            "main_widget": "root",
            "main_classname": self.main_classname,
            "main_menu": "",
            "output_dir": "",
            "output_dir2": "",
            "import_tkvariables": "False",
            "use_ttk_styledefinition_file": "True",
            "use_i18n": "False",
            "all_ids_attributes": "False",
            "generate_code_onsave": "False",
            "use_window_centering_code": "False",
            "ttk_style_definition_file": "styles.py"}.items():
            attribute = ET.SubElement(settings, "setting", {"id": k})
            attribute.text = v

        ET.SubElement(project, "customwidgets")
        return document
