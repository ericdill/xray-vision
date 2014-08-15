from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
from collections import defaultdict
from .util import mapping_mixin
from .. import QtCore, QtGui

from matplotlib.backends.qt4_compat import QtCore, QtGui


class Slider(QtGui.QWidget):
    """
    Fancier version of a slider which includes a label and
    a spinbox
    """
    # export sub-set of slider signals
    # this should be exhaustive eventually
    valueChanged = QtCore.Signal(int)
    rangeChanged = QtCore.Signal(int, int)

    # todo make more things configurable
    def __init__(self, label_text, min_v, max_v, tracking=True):
        super(Slider, self).__init__()
        self._label = QtGui.QLabel(label_text)

        # set up slider
        self._slider = QtGui.QSlider(parent=self)
        self._slider.setRange(min_v, max_v)
        self._slider.setTracking(tracking)
        self._slider.setSingleStep(1)
        self._slider.setOrientation(QtCore.Qt.Horizontal)
        # internal connections
        self._slider.valueChanged.connect(self.valueChanged)
        self._slider.rangeChanged.connect(self.rangeChanged)
        # make buddy with label
        self._label.setBuddy(self._slider)

        # and its spin box
        self._spinbox = QtGui.QSpinBox(parent=self)
        self._spinbox.setRange(self._slider.minimum(), self._slider.maximum())
        self._spinbox.valueChanged.connect(self._slider.setValue)
        self._slider.valueChanged.connect(self._spinbox.setValue)
        self._slider.rangeChanged.connect(self._spinbox.setRange)

        # make layout
        self._layout = QtGui.QHBoxLayout()
        layout = self._layout
        # add widegts
        layout.addWidget(self._label)
        layout.addWidget(self._slider)
        layout.addWidget(self._spinbox)

        self.setLayout(layout)

    # TODO make sure all the slots are included
    @QtCore.Slot(int)
    def setValue(self, val):
        # internal call backs will take care of the spinbox
        self._slider.setValue(val)


class DateTimeBox(QtGui.QWidget):
    #todo implement this class
    pass


class ComboBox(QtGui.QWidget):
    activated = QtCore.Signal(str)
    currentIndexChanged = QtCore.Signal(str)
    editTextChanged = QtCore.Signal(str)
    highlighted = QtCore.Signal(str)

    # todo make more things configurable
    def __init__(self, label_text, list_of_strings,
                 default_entry=0, editable=True):
        # pass up the stack
        super(ComboBox, self).__init__()
        # make the label
        self._lab = QtGui.QLabel(label_text)
        # make che cb
        self._cb = QtGui.QComboBox()
        self._cb.setEditable(editable)
        # stash the text
        self._list_of_strings = list_of_strings
        # shove in the text
        self._cb.addItems(list_of_strings)
        # buddy them up
        self._lab.setBuddy(self._cb)
        # make and set the layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._lab)
        layout.addWidget(self._cb)
        self._layout = layout
        self.setLayout(layout)

        # connect on the signals
        self._cb.activated[str].connect(self.activated)
        self._cb.currentIndexChanged[str].connect(self.currentIndexChanged)
        self._cb.editTextChanged[str].connect(self.editTextChanged)
        self._cb.highlighted[str].connect(self.highlighted)

    # forward the slots
    @QtCore.Slot()
    def clear(self):
        self._cb.clear()

    @QtCore.Slot(int)
    def setCurrentIndex(self, in_val):
        self._cb.setCurrentIndex(in_val)

    @QtCore.Slot(str)
    def setEditText(self, in_str):
        self._cb.setEditText(in_str)

    def getValue(self):
        return self._list_of_strings[self._cb.currentIndex()]


class LineEdit(QtGui.QWidget):
    cursorPositionChanged = QtCore.Signal(int, int)
    editingFinished = QtCore.Signal()
    returnPressed = QtCore.Signal()
    selectionChanged = QtCore.Signal()
    textChanged = QtCore.Signal(str)
    textEdited = QtCore.Signal(str)

    # todo make more things configurable
    def __init__(self, label_text, editable=True):
        # pass up the stack
        super(LineEdit, self).__init__()
        # make the label
        self._lab = QtGui.QLabel(label_text)
        # make che cb
        self._le = QtGui.QLineEdit()
        self._le.setEditable(editable)
        # buddy them up
        self._lab.setBuddy(self._le)
        # make and set the layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._lab)
        layout.addWidget(self._le)
        self._layout = layout
        self.setLayout(layout)

        # connect the signals
        self._le.cursorPositionChanged.connect(self.cursorPositionChanged)
        self._le.editingFinished.connect(self.editingFinished)
        self._le.returnPressed.connect(self.returnPressed)
        self._le.selectionChanged.connect(self.selectionChanged)
        self._le.textChanged.connect(self.textChanged)
        self._le.textEdited.connect(self.textEdited)

    # forward the slots
    @QtCore.Slot()
    def clear(self):
        self._le.clear()

    @QtCore.Slot()
    def copy(self):
        self._le.copy()

    @QtCore.Slot()
    def cut(self):
        self._le.cut()

    @QtCore.Slot()
    def paste(self):
        self._le.paste()

    @QtCore.Slot()
    def redo(self):
        self._le.redo()

    @QtCore.Slot()
    def selectAll(self):
        self._le.selectAll()

    @QtCore.Slot()
    def setText(self, str):
        self._le.setText(str)

    @QtCore.Slot()
    def undo(self):
        self._le.undo()

    def getValue(self):
        # returned as a QString
        text = self._le.text()
        # cast to python string
        text = str(text)
        # check to see if it empty
        if text == '':
            text = None
        return text


class CheckBox(QtGui.QWidget):
    stateChanged = QtCore.Signal()

    # todo make more things configurable
    def __init__(self, label_text, editable=True):
        # pass up the stack
        super(CheckBox, self).__init__()
        # make the label
        self._lab = QtGui.QLabel(label_text)
        # make che cb
        self._check = QtGui.QCheckBox()
        # buddy them up
        self._lab.setBuddy(self._check)
        # make and set the layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._lab)
        layout.addWidget(self._check)
        self._layout = layout
        self.setLayout(layout)

        # connect the signal
        self._check.stateChanged.connect(self.stateChanged)

    # forward the slots
    # no slots to forward

    def getValue(self):
        return self._check.isChecked()


class TripleSpinner(QtGui.QGroupBox):
    """
    A class to wrap up the logic for dealing with a min/max/step
    triple spin box.
    """
    # signal to be emitted when the spin boxes are changed
    # and settled
    valueChanged = QtCore.Signal(float, float)

    def __init__(self, title='', parent=None):
        QtGui.QGroupBox.__init__(self, title, parent=parent)

        self._spinbox_min_intensity = QtGui.QDoubleSpinBox(parent=self)
        self._spinbox_max_intensity = QtGui.QDoubleSpinBox(parent=self)
        self._spinbox_intensity_step = QtGui.QDoubleSpinBox(parent=self)

        ispiner_form = QtGui.QFormLayout()
        ispiner_form.addRow("min", self._spinbox_min_intensity)
        ispiner_form.addRow("max", self._spinbox_max_intensity)
        ispiner_form.addRow("step", self._spinbox_intensity_step)
        self.setLayout(ispiner_form)

    # TODO

    @QtCore.Slot(float, float)
    def setValues(self, bottom, top):
        """
        """
        pass

    @QtCore.Slot(float, float)
    def setLimits(self, bottom, top):
        """
        """
        pass

    @QtCore.Slot(float)
    def setStep(self, step):
        """
        """
        pass

    @property
    def values(self):
        return (self._spinbox_min_intensity.value,
                self._spinbox_max_intensity.value)


class PairSpinner(QtGui.QGroupBox):
    valueChanged = QtCore.Signal(float)
    rangeChanged = QtCore.Signal(float, float)

    def __init__(self, init_min, init_max,
                 init_step, parent=None, title='',
                 value_str=None, step_str=None):
        QtGui.QGroupBox.__init__(self, title, parent=parent)

        if value_str is None:
            value_str = 'value'
        if step_str is None:
            step_str = 'step'

        self._spinbox_value = QtGui.QDoubleSpinBox(parent=self)
        self._spinbox_step = QtGui.QDoubleSpinBox(parent=self)
        self._spinbox_step.valueChanged.connect(
            self._spinbox_value.setSingleStep)

        self._spinbox_value.valueChanged.connect(
            self.valueChanged)

        ispiner_form = QtGui.QFormLayout()
        ispiner_form.addRow(value_str, self._spinbox_value)
        ispiner_form.addRow(step_str, self._spinbox_step)
        self.setLayout(ispiner_form)
        self.setStep(init_step)
        self.setRange(init_min, init_max)

    @QtCore.Slot(float)
    def setStep(self, new_step):
        self._spinbox_step.setValue(new_step)

    @QtCore.Slot(float, float)
    def setRange(self, new_min, new_max):
        self._spinbox_value.setMinimum(new_min)
        self._spinbox_value.setMaximum(new_max)
        self.rangeChanged.emit(new_min, new_max)


class ControlContainer(QtGui.QGroupBox, mapping_mixin):
    _delim = '.'
    _dispatch_map = {'slider': 'create_slider'}

    def create_widget(self, key, type_str, param_dict):
        create_fun_name = self._dispatch_map[type_str]
        create_fun = getattr(self, create_fun_name)
        return create_fun(key, **param_dict)

    def __len__(self):
        print('len')
        return len(list(iter(self)))

    def __contains__(self, key):
        print('contains')
        return key in iter(self)

    def __init__(self, title, parent=None):
        # call parent constructor
        QtGui.QGroupBox.__init__(self, title, parent=parent)

        # nested containers
        self._containers = dict()
        # all non-container contents of this container
        self._contents = dict()

        # specialized listings
        # this is a dict keyed on type of dicts
        # The inner dicts are keyed on name
        self._by_type = defaultdict(dict)

        # make the layout
        self._layout = QtGui.QVBoxLayout()
        # add it to self
        self.setLayout(self._layout)

    def __getitem__(self, key):
        print(key)
        # TODO make this sensible un-wrap KeyException errors
        try:
            # split the key
            split_key = key.strip(self._delim).split(self._delim, 1)
        except TypeError:
            raise KeyError("key is not a string")
        # if one element back -> no splitting needed
        if len(split_key) == 1:
            return self._contents[split_key[0]]
        # else, at least one layer of testing
        else:
            # unpack the key parts
            outer, inner = split_key
            # get the container and pass through the remaining key
            return self._containers[outer][inner]

    def create_container(self, key, container_title=None):
        """
        Create a nested container with in this container

        TODO : add rest of GroupBox parameters

        Parameters
        ----------
        key : str
            The key used to identify this container

        container_title : str or None
            The title of the container.
            If None, defaults to the key.
            If you want to title, use ''

        Returns
        -------
        control_container : ControlContainer
           The container created.
        """
        if container_title is None:
            container_title = key
        control_container = ControlContainer(container_title, parent=self)
        self._layout.addWidget(control_container)
        self._containers[key] = control_container
        return control_container

    def create_button(self, key):
        pass

    def create_checkbox(self, key):
        pass

    def create_combobox(self, key, key_list, editable=True, title=None):
        if title is None:
            title = key
        cb = ComboBox(title, key_list, editable=editable)
        self._add_widget(key, cb)
        return cb

    def create_dict_display(self, key, input_dict):
        pass

    def create_pairspinner(self, key, *args, **kwargs):
        ds = PairSpinner(*args, **kwargs)
        self._add_widget(key, ds)
        return ds

    def create_text(self, key, text):
        """
        Create and add a text label to the control panel
        """
        # create text
        tmp_label = QtGui.QLabel(text)
        self._add_widget(key, tmp_label)

    def create_radiobuttons(self, key):
        pass

    def create_slider(self, key, min_val, max_val, label=None):
        """

        Parameters
        ----------
        """
        if label is None:
            label = key
        # set up slider
        slider = Slider(label, min_val, max_val)
        self._add_widget(key, slider)
        return slider

    def create_triplespinbox(self, key):
        pass

    def _add_widget(self, key, in_widget):
        split_key = key.strip(self._delim).rsplit(self._delim, 1)
        # key is not nested, add to this object
        if len(split_key) == 1:
            key = split_key[0]
            # add to the type dict
            self._by_type[type(in_widget)][key] = in_widget
            # add to the contents list
            self._contents[key] = in_widget
            # add to layout
            self._layout.addWidget(in_widget)
        # else, grab the nested container and add it to that
        else:
            container, key = split_key
            self[container]._add_widget(key, in_widget)

    def iter_containers(self):
        return self._iter_helper_container([])

    def get_container(self, key):
        """
        Get a (possibly nested) container (the normal
        iterator skips these).  We may end up with two
        parallel sets of mapping functions.
        """
        split_key = key.strip(self._delim).rsplit(self._delim, 1)
        if len(split_key) == 1:
            return self._containers[split_key[0]]
        return self._containers[split_key[0]].get_containers(split_key[1])

    def _iter_helper(self, cur_path_list):
        """
        Recursively (depth-first) walk the tree and return the names
        of the leaves

        Parameters
        ----------
        cur_path_list : list of str
            A list of the current path
        """
        for k, v in six.iteritems(self._containers):
            for inner_v in v._iter_helper(cur_path_list + [k]):
                yield inner_v
        for k in six.iterkeys(self._contents):
            yield self._delim.join(cur_path_list + [k])

    def _iter_helper_container(self, cur_path_list):
        """
        Recursively (depth-first) walk the tree and return the names
        of the containers

        Parameters
        ----------
        cur_path_list : list of str
            A list of the current path
        """
        for k, v in six.iteritems(self._containers):
            for inner_v in v._iter_helper_container(cur_path_list + [k]):
                yield inner_v
        if len(cur_path_list):
            yield self._delim.join(cur_path_list)

    def __iter__(self):
        return self._iter_helper([])

    def addStretch(self):
        self._layout.addStretch()


class DictDisplay(QtGui.QGroupBox):
    """
    A generic widget for displaying dictionaries

    Parameters
    ----------
    title : string
       Widget title

    ignore_list : iterable or None
        keys to ignore

    parent : QWidget or None
        Parent widget, passed up stack
    """
    def __init__(self, title, ignore_list=None, parent=None):
        # pass up the stack, GroupBox takes care of the title
        QtGui.QGroupBox.__init__(self, title, parent=parent)

        if ignore_list is None:
            ignore_list = ()
        # make layout
        self.full_layout = QtGui.QVBoxLayout()
        # set layout
        self.setLayout(self.full_layout)
        # make a set of the ignore list
        self._ignore = set(ignore_list)
        self._disp_table = []

    @QtCore.Slot(dict)
    def update(self, in_dict):
        """
        updates the table

        Parameters
        ----------
        in_dict : dict
            The dictionary to display
        """
        # remove everything that is there
        for c in self._disp_table:
            c.deleteLater()

        # make a new list
        self._disp_table = []

        # add the keys alphabetically
        for k, v in sorted(list(in_dict.iteritems())):
            # if key in the ignore list, continue
            if k in self._ignore:
                continue
            self._add_row(k, v)

    def _add_row(self, k, v):
        """
        Private function

        Adds a row to the table

        Parameters
        ----------
        k : object
           The key

        v : object
           The value
        """
        # make a widget for our row
        tmp_widget = QtGui.QWidget(self)
        tmp_layout = QtGui.QHBoxLayout()
        tmp_widget.setLayout(tmp_layout)

        # add the key and value to the row widget
        tmp_layout.addWidget(QtGui.QLabel(str(k) + ':'))
        tmp_layout.addStretch()
        tmp_layout.addWidget(QtGui.QLabel(str(v)))

        # add the row widget to the full layout
        self.full_layout.addWidget(tmp_widget)
        # add the row widget to
        self._disp_table.append(tmp_widget)
