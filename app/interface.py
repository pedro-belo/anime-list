import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk

from config import APP_NAME
import facade

screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path('./rsrc/style.css')
Gtk.StyleContext.add_provider_for_screen(
    screen, provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

class Dialog(Gtk.Dialog):

    def __init__(self, parent, action, **kwargs):

        Gtk.Dialog.__init__(self, title='...', transient_for=parent, flags=0)

        self.action = action

    def create_grid(self):
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        self.get_content_area().add(grid)

        self.grid = grid

    def create_title(self):
        title = Gtk.Label(margin=10)
        title.set_markup(f"<big><b>{self.dialog_title}</b></big>")
        self.grid.attach(title, 0, 0 , 6, 1)

    def create_entry(self, text='', default_value=''):

        label = Gtk.Label()
        label.set_label(text)
        label.set_justify(Gtk.Justification.LEFT)

        entry = Gtk.Entry()
        entry.set_text(default_value)

        return label, entry

    def create_entry_title(self):

        title = self.fields.get('titulo', '')

        label, entry = self.create_entry('Title: ', title)

        self.grid.attach(label, 0, 1, 2, 1)
        self.grid.attach(entry, 2, 1, 6, 1)

        self.entry_titulo = entry

    def create_entry_episodio_atual(self):

        episodio_atual = str(self.fields.get('episodio_atual', 0))

        label, entry = self.create_entry('Episodio Atual: ', episodio_atual)

        self.grid.attach(label, 0, 2, 2, 1)
        self.grid.attach(entry, 2, 2, 6, 1)

        self.entry_episodio_atual = entry

    def create_entry_total_episodios(self):

        total_episodios = str(self.fields.get('total_episodios', 0))

        label, entry = self.create_entry('Total Episodios: ', total_episodios)

        self.grid.attach(label, 0, 3, 2, 1)
        self.grid.attach(entry, 2, 3, 6, 1)

        self.entry_total_episodios = entry

    def create_select_status(self):

        label = Gtk.Label()
        label.set_label('Progresso')
        label.set_justify(Gtk.Justification.LEFT)

        select_choices = Gtk.ComboBoxText()
        for choice in facade.get_status_choices():

            choice_id, choice_text = choice
            select_choices.append(str(choice_id), choice_text)

        stauts = self.fields.get('status', None)
        if stauts:
            choice_selected, _ = stauts
            select_choices.set_active_id(str(choice_selected))

        self.grid.attach(label, 0, 4, 2, 1)
        self.grid.attach(select_choices, 2, 4, 6, 1)

        self.select_choices = select_choices

    def cancel(self, button):
        self.destroy()

    def execute(self, button):

        anime = {}

        try:

            anime['titulo'] = str(self.entry_titulo.get_text())
            anime['total_episodios'] = int(self.entry_total_episodios.get_text())
            anime['episodio_atual'] = int(self.entry_episodio_atual.get_text())
            anime['status_id'] = int(self.select_choices.get_active_id())
            if self._pk:
                anime['pk'] = int(self._pk)

        except Exception as e:
            print('Houve um erro...', e)
            return

        self.action(**anime)
        self.destroy()

    def create_buttons(self):

        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.HORIZONTAL)

        button_cancel = Gtk.Button(label='Cancelar')
        button_cancel.set_name('button-status')
        button_cancel.connect('clicked', self.cancel)

        box.pack_start(button_cancel, True, True, 0)

        button_execute = Gtk.Button.new_with_label(self.action_title)
        button_execute.connect('clicked', self.execute)
        button_execute.set_name('button-status')

        box.pack_start(button_execute, True, True, 0)

        self.grid.attach(box, 2, 5, 6, 1)

    def build(self):

        self.create_grid()

        self.create_title()

        self.create_entry_title()

        self.create_entry_episodio_atual()

        self.create_entry_total_episodios()

        self.create_select_status()

        self.create_buttons()

        self.show_all()


class CreateAnime(Dialog):
    
    dialog_title = 'Cadastro Anime'
    action_title = 'Salvar'

    def __init__(self, parent, action, **kwargs):

        self._pk = None
        self.fields = {}

        super().__init__(parent, action, **kwargs)


class UpdateAnime(Dialog):

    action_title = 'Salvar alterações'
    dialog_title = 'Atualizar Anime'

    def __init__(self, parent, action, **kwargs):

        self._pk = kwargs.get('pk')
        self.fields = facade.get(self._pk)

        super().__init__(parent, action, **kwargs)


class AnimeListGUI(Gtk.Window):

    container = None
    container_items = None
    container_title = None
    status_id = None

    def __init__(self):
        Gtk.Window.__init__(self, title=APP_NAME, resizable=False)
        self.set_default_size(0, 520)

    def create_grid(self):

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_name('main-grid')
        self.add(grid)

        self.grid = grid

    def create_buttons_status(self):

        button = Gtk.Button(label='Todos')
        self.grid.attach(button, 0, 0, 1, 1)
        button.connect('clicked', self.load_items_by_status, None)
        button.set_name('button-status')

        deslocamento = 1
        for choice in facade.get_status_choices():

            status_id, status_text = choice    

            button = Gtk.Button(label=status_text)
            button.set_name('button-status')
            button.connect('clicked', self.load_items_by_status, status_id)
            self.grid.attach(button, deslocamento, 0, 1, 1)

            deslocamento += 1

        self.max_width = deslocamento

    def create_separator(self):
        separator = Gtk.Separator(margin=10)
        self.grid.attach(separator, 0, 2, self.max_width, 1)

    def create_title(self):
        title = Gtk.Label(margin_top=10)
        title.set_markup("<big><b>Lista Animes</b></big>")
        title.set_justify(Gtk.Justification.CENTER)

        self.grid.attach(title, 0, 1, self.max_width, 1)

        self.title = title

    def create_grid_anime_list(self):

        grid_anime_list = Gtk.Grid()
        grid_anime_list.set_column_homogeneous(True)
        scroll = Gtk.ScrolledWindow(vexpand=True)
        scroll.add(grid_anime_list)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)


        self.grid.attach(scroll, 0, 3, self.max_width, 8)
        self.grid_anime_list = grid_anime_list
        self.scroll = scroll

        self.grid.show_all()
        self.grid_anime_list.show_all()

    def create_button_add(self):
        button = Gtk.Button(label='Adicionar Novo', margin=8)
        button.set_name('button-status')
        button.connect('clicked', self.add_item)

        self.grid.attach(button, 0, 11, self.max_width, 1)

    def load_items(self):

        items = facade.get_list() if self.status_id is None else facade.get_list_by_status(self.status_id)

        self.destroy_grid_items()
        linha = 0
        for item in items:

            grid_item = self.create_grid_item(
                item['id'],
                item['titulo'],
                item['episodio_atual'],
                item['total_episodios']
            )

            self.grid_anime_list.attach(grid_item, 0, linha, 1, 1)
            self.grid_anime_list.show_all()

            linha += 1


    def add_item(self, button):
        dialog = CreateAnime(parent=self, action=facade.create)
        dialog.build()
        dialog.run()
        dialog.destroy()
        self.load_items()

    def update_item(self, button, pk):
        dialog = UpdateAnime(parent=self, action=facade.update, pk=pk)
        dialog.build()
        dialog.run()
        dialog.destroy()
        self.load_items()

    def destroy_grid_items(self):
        for child in self.grid_anime_list.get_children():
            self.grid_anime_list.remove(child) 

    def create_grid_item(self, pk, titulo, episodio_atual, total_episodios):

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box.set_homogeneous(True)

        label = Gtk.Label(label=titulo)
        label.set_justify(Gtk.Justification.LEFT)
        box.pack_start(label, True, True, 0)

        label = Gtk.Label(label=str(episodio_atual))
        label.set_justify(Gtk.Justification.LEFT)
        box.pack_start(label, True, True, 0)

        label = Gtk.Label(label=str(total_episodios))
        box.pack_start(label, True, True, 0)

        box_options = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        button_delete = Gtk.Button.new_with_label('🗑')
        button_delete.set_name('button-delete')
        button_delete.connect('clicked', self.delete_item, pk)
        box_options.pack_start(button_delete, True, True, 0)

        button_update = Gtk.Button.new_with_label('🖋')
        button_update.set_name('button-update')

        box_options.pack_start(button_update, True, True, 0)
        button_update.connect('clicked', self.update_item, pk)
  
        box.pack_start(box_options, True, True, 0)

        return box

    def delete_item(self, button, pk):
        facade.delete(pk)
        self.load_items()

    def load_items_by_status(self, button, status_id):
        self.status_id = status_id
        self.load_items()

    def build(self):

        self.create_grid()

        self.create_buttons_status()
        
        self.create_title()

        self.create_separator()
        
        self.create_grid_anime_list()

        self.load_items()
        
        self.create_button_add()

if __name__ == '__main__':

    window = AnimeListGUI()
    window.connect("destroy", Gtk.main_quit)
    window.build()
    window.show_all()
    Gtk.main()
