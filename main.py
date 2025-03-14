from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.spinner import Spinner
import os
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*AppColors.BACKGROUND)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_bg, pos=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos


# Set app theme colors
class AppColors:
    PRIMARY = [0.4, 0.7, 1, 1]
    SECONDARY = [1, 0.7, 0.6, 1]
    BACKGROUND = [0.85, 0.93, 1, 1]
    TEXT = [0.2, 0.2, 0.3, 1]

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

recipes_store = JsonStore(os.path.join(data_dir, 'recipes.json'))
menu_store = JsonStore(os.path.join(data_dir, 'menu.json'))
shopping_list_store = JsonStore(os.path.join(data_dir, 'shopping_list.json'))

class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text='Cuisine Assistant', font_size=24, size_hint_y=None, height=50, color=AppColors.TEXT)
        layout.add_widget(title)
        
        # Buttons for navigation
        recipes_btn = Button(text='Recettes', size_hint_y=None, height=60, 
                            background_color=AppColors.PRIMARY)
        recipes_btn.bind(on_press=self.go_to_recipes)
        
        menu_btn = Button(text='Menu de la semaine', size_hint_y=None, height=60,
                         background_color=AppColors.PRIMARY)
        menu_btn.bind(on_press=self.go_to_menu)
        
        shopping_btn = Button(text='Liste de courses', size_hint_y=None, height=60,
                             background_color=AppColors.PRIMARY)
        shopping_btn.bind(on_press=self.go_to_shopping)
        
        layout.add_widget(recipes_btn)
        layout.add_widget(menu_btn)
        layout.add_widget(shopping_btn)
        
        self.add_widget(layout)
    
    def go_to_recipes(self, instance):
        self.manager.current = 'recipes'
    
    def go_to_menu(self, instance):
        self.manager.current = 'menu'
    
    def go_to_shopping(self, instance):
        self.manager.current = 'shopping'

class RecipesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(RecipesScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        title = Label(text='Recettes', color=AppColors.TEXT)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Add new recipe button
        add_btn = Button(text='Ajouter une recette', size_hint_y=None, height=50,
                        background_color=AppColors.PRIMARY)
        add_btn.bind(on_press=self.add_recipe)
        
        # Recipe list
        self.recipe_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.recipe_list.bind(minimum_height=self.recipe_list.setter('height'))
        
        scroll = ScrollView()
        scroll.add_widget(self.recipe_list)
        
        self.layout.add_widget(header)
        self.layout.add_widget(add_btn)
        self.layout.add_widget(scroll)
        
        self.add_widget(self.layout)
        
    def on_pre_enter(self):
        self.load_recipes()
    
    def load_recipes(self):
        self.recipe_list.clear_widgets()
        if recipes_store.count() == 0:
            self.recipe_list.add_widget(Label(text='Aucune recette enregistrée', size_hint_y=None, height=40, color=AppColors.TEXT))
        else:
            for recipe_name in recipes_store.keys():
                recipe_btn = Button(text=recipe_name, size_hint_y=None, height=50, 
                                   background_color=AppColors.PRIMARY)
                recipe_btn.bind(on_press=lambda btn, name=recipe_name: self.view_recipe(name))
                self.recipe_list.add_widget(recipe_btn)
    
    def add_recipe(self, instance):
        self.manager.current = 'add_recipe'
    
    def view_recipe(self, recipe_name):
        self.manager.get_screen('view_recipe').recipe_name = recipe_name
        self.manager.current = 'view_recipe'
    
    def go_back(self, instance):
        self.manager.current = 'home'

class AddRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(AddRecipeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        title = Label(text='Ajouter une recette', color=AppColors.TEXT)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Content layout
        content_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Recipe name
        name_layout = BoxLayout(size_hint_y=None, height=50)
        name_layout.add_widget(Label(text='Nom de la recette:', size_hint_x=None, width=150, color=AppColors.TEXT))
        self.name_input = TextInput(multiline=False)
        name_layout.add_widget(self.name_input)
        
        # Number of servings
        servings_layout = BoxLayout(size_hint_y=None, height=50)
        servings_layout.add_widget(Label(text='Nombre de personnes:', size_hint_x=None, width=150, color=AppColors.TEXT))
        self.servings_input = TextInput(multiline=False, text='4')
        servings_layout.add_widget(self.servings_input)
        
        # Ingredients
        ingredients_label = Label(text='Ingrédients:', size_hint_y=None, height=30, halign='left', color=AppColors.TEXT)
        ingredients_label.bind(size=ingredients_label.setter('text_size'))
        
        # Container for ingredients
        ingredients_container = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        
        # Scrollable ingredients layout
        self.ingredients_scroll = ScrollView(size_hint=(1, 1))
        self.ingredients_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.ingredients_layout.bind(minimum_height=self.ingredients_layout.setter('height'))
        self.ingredients_scroll.add_widget(self.ingredients_layout)
        
        # Add first ingredient row
        self.add_ingredient_row()
        
        ingredients_container.add_widget(self.ingredients_scroll)
        
        # Add ingredient button
        add_ingredient_btn = Button(text='Ajouter un ingrédient', size_hint_y=None, height=50,
                                   background_color=AppColors.PRIMARY)
        add_ingredient_btn.bind(on_press=self.add_ingredient_row)
        
        # Instructions
        instructions_label = Label(text='Instructions:', size_hint_y=None, height=30, halign='left', color=AppColors.TEXT)
        instructions_label.bind(size=instructions_label.setter('text_size'))
        self.instructions_input = TextInput(height=100, size_hint_y=None, multiline=True)
        
        # Save button
        save_btn = Button(text='Enregistrer la recette', size_hint_y=None, height=50,
                         background_color=AppColors.PRIMARY)
        save_btn.bind(on_press=self.save_recipe)
        
        # Add widgets to content layout
        content_layout.add_widget(name_layout)
        content_layout.add_widget(servings_layout)
        content_layout.add_widget(ingredients_label)
        content_layout.add_widget(ingredients_container)
        content_layout.add_widget(add_ingredient_btn)
        content_layout.add_widget(instructions_label)
        content_layout.add_widget(self.instructions_input)
        content_layout.add_widget(save_btn)
        
        # Main scroll view
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(content_layout)
        
        self.layout.add_widget(header)
        self.layout.add_widget(scroll)
        
        self.add_widget(self.layout)

        
    
    def add_ingredient_row(self, instance=None):
        # Create a BoxLayout for the ingredient row
        row_layout = BoxLayout(
            orientation='horizontal',
            spacing=5,
            size_hint_y=None,
            height=40
        )
        
        # Create the input fields with appropriate size hints
        name_input = TextInput(
            hint_text='Ingrédient',
            multiline=False,
            size_hint=(0.5, None),
            height=40
        )
        quantity_input = TextInput(
            hint_text='Quantité',
            multiline=False,
            size_hint=(0.25, None),
            height=40
        )
        unit_input = TextInput(
            hint_text='Unité',
            multiline=False,
            size_hint=(0.25, None),
            height=40
        )
        
        # Add the inputs to the row layout
        row_layout.add_widget(name_input)
        row_layout.add_widget(quantity_input)
        row_layout.add_widget(unit_input)
        
        # Add the row to the ingredients layout
        self.ingredients_layout.add_widget(row_layout)

    def save_recipe(self, instance):
        recipe_name = self.name_input.text.strip()
        if not recipe_name:
            return
        
        servings = self.servings_input.text.strip()
        if not servings.isdigit():
            servings = "4"  # Default to 4 if not a valid number
        
        ingredients = []
        # Process ingredients in groups of 3 (name, quantity, unit)
        for i in range(0, len(self.ingredients_layout.children), 3):
            if i+2 < len(self.ingredients_layout.children):
                name = self.ingredients_layout.children[i+2].text.strip()
                quantity = self.ingredients_layout.children[i+1].text.strip()
                unit = self.ingredients_layout.children[i].text.strip()
                
                if name:
                    ingredients.append({
                        'name': name,
                        'quantity': quantity,
                        'unit': unit
                    })
        
        instructions = self.instructions_input.text.strip()
        
        recipes_store.put(recipe_name, ingredients=ingredients, instructions=instructions, servings=servings)
        
        self.go_back(None)
    
    def go_back(self, instance):
        self.manager.current = 'recipes'

class ViewRecipeScreen(BaseScreen):
    recipe_name = StringProperty('')
    servings_display = NumericProperty(0)
    original_servings = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(ViewRecipeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        self.header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        self.title_label = Label(text='', color=AppColors.TEXT)
        
        self.header.add_widget(back_btn)
        self.header.add_widget(self.title_label)
        
        # Content layout
        self.content_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        # Scroll view
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.content_layout)
        
        self.layout.add_widget(self.header)
        self.layout.add_widget(scroll)
        
        self.add_widget(self.layout)
        
        # Initialize ingredient labels list
        self.ingredient_labels = []
    
    def on_pre_enter(self):
        self.load_recipe()
    
    def load_recipe(self):
        self.content_layout.clear_widgets()
        self.title_label.text = self.recipe_name
        self.ingredient_labels = []
        
        if recipes_store.exists(self.recipe_name):
            recipe = recipes_store.get(self.recipe_name)
            
            # Servings
            servings_layout = BoxLayout(size_hint_y=None, height=50)
            servings_layout.add_widget(Label(text='Nombre de personnes:', size_hint_x=None, width=150, color=AppColors.TEXT))
            
            self.original_servings = int(recipe.get('servings', '4'))
            self.servings_display = self.original_servings
            
            servings_controls = BoxLayout(size_hint_x=None, width=150)
            decrease_btn = Button(text='-', size_hint_x=None, width=40, background_color=AppColors.SECONDARY)
            decrease_btn.bind(on_press=self.decrease_servings)
            
            self.servings_label = Label(text=str(self.servings_display), size_hint_x=None, width=70, color=AppColors.TEXT)
            
            increase_btn = Button(text='+', size_hint_x=None, width=40, background_color=AppColors.SECONDARY)
            increase_btn.bind(on_press=self.increase_servings)
            
            servings_controls.add_widget(decrease_btn)
            servings_controls.add_widget(self.servings_label)
            servings_controls.add_widget(increase_btn)
            
            servings_layout.add_widget(servings_controls)
            self.content_layout.add_widget(servings_layout)
            
            # Ingredients
            ingredients_title = Label(text='Ingrédients:', size_hint_y=None, height=40, 
                                   font_size=18, halign='left', color=AppColors.TEXT)
            ingredients_title.bind(size=ingredients_title.setter('text_size'))
            self.content_layout.add_widget(ingredients_title)
            
            for ingredient in recipe['ingredients']:
                ingredient_layout = BoxLayout(size_hint_y=None, height=30)
                text = f"{ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}"
                ingredient_label = Label(text=text, halign='left', color=AppColors.TEXT)
                ingredient_label.bind(size=ingredient_label.setter('text_size'))
                self.ingredient_labels.append((ingredient_label, ingredient))
                ingredient_layout.add_widget(ingredient_label)
                self.content_layout.add_widget(ingredient_layout)
            
            # Instructions
            instructions_title = Label(text='Instructions:', size_hint_y=None, height=40,
                                    font_size=18, halign='left', color=AppColors.TEXT)
            instructions_title.bind(size=instructions_title.setter('text_size'))
            self.content_layout.add_widget(instructions_title)
            
            instructions_text = recipe['instructions'] if recipe['instructions'] else "Pas d'instructions"
            instructions_label = Label(text=instructions_text, size_hint_y=None,
                                    halign='left', color=AppColors.TEXT)
            instructions_label.bind(size=instructions_label.setter('text_size'))
            
            # Set a minimum height for instructions
            instructions_label.height = 100
            self.content_layout.add_widget(instructions_label)
            
            # Edit and delete buttons
            buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
            
            edit_btn = Button(text='Modifier', background_color=AppColors.PRIMARY)
            edit_btn.bind(on_press=self.edit_recipe)
            
            delete_btn = Button(text='Supprimer', background_color=AppColors.SECONDARY)
            delete_btn.bind(on_press=self.delete_recipe)
            
            buttons_layout.add_widget(edit_btn)
            buttons_layout.add_widget(delete_btn)
            
            self.content_layout.add_widget(buttons_layout)
    
    def update_ingredient_quantities(self):
        if self.original_servings > 0:
            ratio = self.servings_display / self.original_servings
            for label, ingredient in self.ingredient_labels:
                try:
                    original_quantity = float(ingredient['quantity'])
                    new_quantity = original_quantity * ratio
                    # Format to avoid too many decimal places
                    if new_quantity == int(new_quantity):
                        new_quantity = int(new_quantity)
                    else:
                        new_quantity = round(new_quantity, 2)
                    
                    text = f"{ingredient['name']}: {new_quantity} {ingredient['unit']}"
                    label.text = text
                except (ValueError, TypeError):
                    # If quantity is not a number, leave it as is
                    pass
    
    def increase_servings(self, instance):
        self.servings_display += 1
        self.servings_label.text = str(self.servings_display)
        self.update_ingredient_quantities()
    
    def decrease_servings(self, instance):
        if self.servings_display > 1:
            self.servings_display -= 1
            self.servings_label.text = str(self.servings_display)
            self.update_ingredient_quantities()
    
    def edit_recipe(self, instance):
        self.manager.get_screen('edit_recipe').recipe_name = self.recipe_name
        self.manager.current = 'edit_recipe'
    
    def delete_recipe(self, instance):
        if recipes_store.exists(self.recipe_name):
            recipes_store.delete(self.recipe_name)
        self.go_back(None)
    
    def go_back(self, instance):
        self.manager.current = 'recipes'

class EditRecipeScreen(BaseScreen):
    recipe_name = StringProperty('')
    
    def __init__(self, **kwargs):
        super(EditRecipeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        self.title_label = Label(text='Modifier la recette', color=AppColors.TEXT)
        
        header.add_widget(back_btn)
        header.add_widget(self.title_label)
        
        # Content layout
        content_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Recipe name
        name_layout = BoxLayout(size_hint_y=None, height=50)
        name_layout.add_widget(Label(text='Nom de la recette:', size_hint_x=None, width=150, color=AppColors.TEXT))
        self.name_input = TextInput(multiline=False)
        name_layout.add_widget(self.name_input)
        
        # Number of servings
        servings_layout = BoxLayout(size_hint_y=None, height=50)
        servings_layout.add_widget(Label(text='Nombre de personnes:', size_hint_x=None, width=150, color=AppColors.TEXT))
        self.servings_input = TextInput(multiline=False)
        servings_layout.add_widget(self.servings_input)
        
        # Ingredients
        ingredients_label = Label(text='Ingrédients:', size_hint_y=None, height=30, halign='left', color=AppColors.TEXT)
        ingredients_label.bind(size=ingredients_label.setter('text_size'))
        
        # Container for ingredients
        ingredients_container = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        
        # Scrollable ingredients layout
        self.ingredients_scroll = ScrollView(size_hint=(1, 1))
        self.ingredients_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.ingredients_layout.bind(minimum_height=self.ingredients_layout.setter('height'))
        self.ingredients_scroll.add_widget(self.ingredients_layout)
        
        ingredients_container.add_widget(self.ingredients_scroll)
        
        # Add ingredient button
        add_ingredient_btn = Button(text='Ajouter un ingrédient', size_hint_y=None, height=50,
                                   background_color=AppColors.PRIMARY)
        add_ingredient_btn.bind(on_press=self.add_ingredient_row)

        # Bouton pour exporter en PDF
        export_pdf_btn = Button(text='Exporter en PDF', size_hint_y=None, height=50, background_color=AppColors.PRIMARY)
        export_pdf_btn.bind(on_press=self.export_to_pdf)

        # Ajouter le bouton en bas de l'interface
        content_layout.add_widget(export_pdf_btn)
        
        # Instructions
        instructions_label = Label(text='Instructions:', size_hint_y=None, height=30, halign='left', color=AppColors.TEXT)
        instructions_label.bind(size=instructions_label.setter('text_size'))
        self.instructions_input = TextInput(height=100, size_hint_y=None, multiline=True)
        
        # Save button
        save_btn = Button(text='Enregistrer les modifications', size_hint_y=None, height=50,
                         background_color=AppColors.PRIMARY)
        save_btn.bind(on_press=self.save_recipe)
        
        # Add widgets to content layout
        content_layout.add_widget(name_layout)
        content_layout.add_widget(servings_layout)
        content_layout.add_widget(ingredients_label)
        content_layout.add_widget(ingredients_container)
        content_layout.add_widget(add_ingredient_btn)
        content_layout.add_widget(instructions_label)
        content_layout.add_widget(self.instructions_input)
        content_layout.add_widget(save_btn)
        
        # Main scroll view
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(content_layout)
        
        self.layout.add_widget(header)
        self.layout.add_widget(scroll)
        
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        self.load_recipe()
    
    def load_recipe(self):
        self.ingredients_layout.clear_widgets()
        
        if recipes_store.exists(self.recipe_name):
            recipe = recipes_store.get(self.recipe_name)
            
            self.name_input.text = self.recipe_name
            self.servings_input.text = recipe.get('servings', '4')
            self.instructions_input.text = recipe.get('instructions', '')
            
            for ingredient in recipe.get('ingredients', []):
                self.add_ingredient_row(None, ingredient)
    
    def add_ingredient_row(self, instance=None, ingredient=None):
        row_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height=40)

        name_input = TextInput(hint_text='Ingrédient', multiline=False, size_hint=(0.5, None), height=40)
        quantity_input = TextInput(hint_text='Quantité', multiline=False, size_hint=(0.25, None), height=40)
        unit_input = TextInput(hint_text='Unité', multiline=False, size_hint=(0.25, None), height=40)

        if ingredient:
            name_input.text = ingredient.get('name', '')
            quantity_input.text = ingredient.get('quantity', '')
            unit_input.text = ingredient.get('unit', '')

        row_layout.add_widget(name_input)
        row_layout.add_widget(quantity_input)
        row_layout.add_widget(unit_input)

        self.ingredients_layout.add_widget(row_layout)

    
    def save_recipe(self, instance):
        new_recipe_name = self.name_input.text.strip()
        if not new_recipe_name:
            return
        
        servings = self.servings_input.text.strip()
        if not servings.isdigit():
            servings = "4"  # Default to 4 if not a valid number
        
        ingredients = []
        # Process ingredients in groups of 3 (name, quantity, unit)
        for i in range(0, len(self.ingredients_layout.children), 3):
            if i+2 < len(self.ingredients_layout.children):
                name = self.ingredients_layout.children[i+2].text.strip()
                quantity = self.ingredients_layout.children[i+1].text.strip()
                unit = self.ingredients_layout.children[i].text.strip()
                
                if name:
                    ingredients.append({
                        'name': name,
                        'quantity': quantity,
                        'unit': unit
                    })
        
        instructions = self.instructions_input.text.strip()
        
        # Delete old recipe if name changed
        if new_recipe_name != self.recipe_name and recipes_store.exists(self.recipe_name):
            recipes_store.delete(self.recipe_name)
        
        # Save new recipe
        recipes_store.put(new_recipe_name, ingredients=ingredients, instructions=instructions, servings=servings)
        
        # Update menu if this recipe was used
        for day in menu_store.keys():
            day_data = menu_store.get(day)
            for meal_time in ['breakfast', 'lunch', 'dinner']:
                if meal_time in day_data and isinstance(day_data[meal_time], list):
                    meals = day_data[meal_time]
                    for i, meal in enumerate(meals):
                        if meal == self.recipe_name:
                            meals[i] = new_recipe_name
                    day_data[meal_time] = meals
            menu_store.put(day, **day_data)
        
        self.go_back(None)
    
    def go_back(self, instance):
        self.manager.current = 'view_recipe'
    

    def export_to_pdf(self, instance):
        if not self.recipe_name:
            return

        recipe_data = recipes_store.get(self.recipe_name)
        pdf_filename = f"{self.recipe_name.replace(' ', '_')}.pdf"
        pdf_path = os.path.join(os.path.expanduser("~"), pdf_filename)  # Sauvegarde dans le dossier utilisateur

        # Création du PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Titre de la recette
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, f"Recette : {self.recipe_name}")

        # Nombre de personnes
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 80, f"Nombre de personnes : {recipe_data.get('servings', '4')}")

        # Ingrédients
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 110, "Ingrédients :")

        y_position = height - 130
        c.setFont("Helvetica", 12)
        for ingredient in recipe_data.get("ingredients", []):
            ingredient_text = f"- {ingredient['name']}: {ingredient['quantity']} {ingredient['unit']}"
            c.drawString(120, y_position, ingredient_text)
            y_position -= 20  # Espacement entre les lignes

        # Instructions
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y_position - 20, "Instructions :")

        y_position -= 40
        c.setFont("Helvetica", 12)
        instructions = recipe_data.get("instructions", "Pas d'instructions")
        for line in instructions.split("\n"):
            c.drawString(120, y_position, line)
            y_position -= 20  # Espacement entre les lignes

        c.save()  # Sauvegarde le PDF

class MenuScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        title = Label(text='Menu de la semaine', color=AppColors.TEXT)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Days of the week
        self.days_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.days_layout.bind(minimum_height=self.days_layout.setter('height'))
        
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        for day in days:
            day_layout = GridLayout(cols=1, size_hint_y=None, height=150, spacing=5)
            day_layout.add_widget(Label(text=day, size_hint_y=None, height=30, font_size=18, color=AppColors.TEXT))
            
            # Breakfast
            breakfast_layout = BoxLayout(size_hint_y=None, height=30)
            breakfast_layout.add_widget(Label(text='Petit déjeuner:', size_hint_x=None, width=100, color=AppColors.TEXT))
            breakfast_btn = Button(text='Choisir un repas', background_color=AppColors.PRIMARY)
            breakfast_btn.bind(on_press=lambda btn, d=day, m='breakfast': self.choose_meal(d, m))
            breakfast_layout.add_widget(breakfast_btn)
            day_layout.add_widget(breakfast_layout)
            
            # Lunch
            lunch_layout = BoxLayout(size_hint_y=None, height=30)
            lunch_layout.add_widget(Label(text='Déjeuner:', size_hint_x=None, width=100, color=AppColors.TEXT))
            lunch_btn = Button(text='Choisir un repas', background_color=AppColors.PRIMARY)
            lunch_btn.bind(on_press=lambda btn, d=day, m='lunch': self.choose_meal(d, m))
            lunch_layout.add_widget(lunch_btn)
            day_layout.add_widget(lunch_layout)
            
            # Dinner
            dinner_layout = BoxLayout(size_hint_y=None, height=30)
            dinner_layout.add_widget(Label(text='Dîner:', size_hint_x=None, width=100, color=AppColors.TEXT))
            dinner_btn = Button(text='Choisir un repas', background_color=AppColors.PRIMARY)
            dinner_btn.bind(on_press=lambda btn, d=day, m='dinner': self.choose_meal(d, m))
            dinner_layout.add_widget(dinner_btn)
            day_layout.add_widget(dinner_layout)
            
            self.days_layout.add_widget(day_layout)
        
        # Generate shopping list button
        generate_btn = Button(text='Générer la liste de courses', size_hint_y=None, height=50,
                             background_color=AppColors.PRIMARY)
        generate_btn.bind(on_press=self.generate_shopping_list)
        
        scroll = ScrollView()
        scroll.add_widget(self.days_layout)
        
        self.layout.add_widget(header)
        self.layout.add_widget(scroll)
        self.layout.add_widget(generate_btn)
        
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        self.load_menu()
    
    def load_menu(self):
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        for i, day in enumerate(days):
            day_layout = self.days_layout.children[len(days) - 1 - i]
            
            # Get breakfast, lunch, and dinner buttons
            breakfast_layout = day_layout.children[2]
            breakfast_btn = breakfast_layout.children[0]
            
            lunch_layout = day_layout.children[1]
            lunch_btn = lunch_layout.children[0]
            
            dinner_layout = day_layout.children[0]
            dinner_btn = dinner_layout.children[0]
            
            if menu_store.exists(day):
                day_data = menu_store.get(day)
                
                if 'breakfast' in day_data and day_data['breakfast']:
                    breakfast_btn.text = ', '.join(day_data['breakfast'])
                else:
                    breakfast_btn.text = 'Choisir un repas'
                
                if 'lunch' in day_data and day_data['lunch']:
                    lunch_btn.text = ', '.join(day_data['lunch'])
                else:
                    lunch_btn.text = 'Choisir un repas'
                
                if 'dinner' in day_data and day_data['dinner']:
                    dinner_btn.text = ', '.join(day_data['dinner'])
                else:
                    dinner_btn.text = 'Choisir un repas'
            else:
                breakfast_btn.text = 'Choisir un repas'
                lunch_btn.text = 'Choisir un repas'
                dinner_btn.text = 'Choisir un repas'
    
    def choose_meal(self, day, meal_time):
        self.manager.get_screen('choose_meal').day = day
        self.manager.get_screen('choose_meal').meal_time = meal_time
        self.manager.current = 'choose_meal'
    
    def generate_shopping_list(self, instance):
        shopping_list = {}
        
        # Collect all ingredients from the menu
        for day in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']:
            if menu_store.exists(day):
                day_data = menu_store.get(day)
                
                for meal_time in ['breakfast', 'lunch', 'dinner']:
                    if meal_time in day_data and isinstance(day_data[meal_time], list):
                        meals = day_data[meal_time]
                        for meal in meals:
                            if recipes_store.exists(meal):
                                recipe = recipes_store.get(meal)
                                
                                for ingredient in recipe.get('ingredients', []):
                                    name = ingredient['name']
                                    quantity = ingredient['quantity']
                                    unit = ingredient['unit']
                                    
                                    if name in shopping_list:
                                        # Try to add quantities if they're numbers
                                        try:
                                            current_quantity = float(shopping_list[name]['quantity'])
                                            additional_quantity = float(quantity)
                                            shopping_list[name]['quantity'] = str(current_quantity + additional_quantity)
                                        except (ValueError, TypeError):
                                            # If conversion fails, just keep the original
                                            pass
                                    else:
                                        shopping_list[name] = {
                                            'quantity': quantity,
                                            'unit': unit,
                                            'checked': False
                                        }
        
        # Save the shopping list
        shopping_list_store.clear()  # Clear existing list
        for item, details in shopping_list.items():
            shopping_list_store.put(item, quantity=details['quantity'], unit=details['unit'], checked=False)
        
        # Go to shopping list screen
        self.manager.current = 'shopping'
    
    def go_back(self, instance):
        self.manager.current = 'home'

class ChooseMealScreen(BaseScreen):
    day = StringProperty('')
    meal_time = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ChooseMealScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        self.header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        self.title_label = Label(text='Choisir un repas', color=AppColors.TEXT)
        
        self.header.add_widget(back_btn)
        self.header.add_widget(self.title_label)
        
        # Search input
        search_layout = BoxLayout(size_hint_y=None, height=50)
        self.search_input = TextInput(hint_text='Rechercher une recette', multiline=False)
        self.search_input.bind(text=self.filter_recipes)
        search_layout.add_widget(self.search_input)
        
        # Recipe list
        self.recipe_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.recipe_list.bind(minimum_height=self.recipe_list.setter('height'))
        
        # Selected meals list
        self.selected_meals_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        self.selected_meals_label = Label(text='Repas sélectionnés:', size_hint_y=None, height=30, color=AppColors.TEXT)
        self.selected_meals = GridLayout(cols=1, spacing=5, size_hint_y=None, height=70)
        self.selected_meals.bind(minimum_height=self.selected_meals.setter('height'))
        
        self.selected_meals_layout.add_widget(self.selected_meals_label)
        self.selected_meals_layout.add_widget(self.selected_meals)
        
        # Custom meal input
        custom_layout = BoxLayout(size_hint_y=None, height=50)
        self.custom_input = TextInput(hint_text='Ou entrez un repas personnalisé', multiline=False)
        custom_btn = Button(text='Ajouter', size_hint_x=None, width=100, 
                           background_color=AppColors.PRIMARY)
        custom_btn.bind(on_press=self.add_custom_meal)
        
        custom_layout.add_widget(self.custom_input)
        custom_layout.add_widget(custom_btn)
        
        # Save button
        save_btn = Button(text='Enregistrer les repas', size_hint_y=None, height=50,
                         background_color=AppColors.PRIMARY)
        save_btn.bind(on_press=self.save_meals)
        
        scroll = ScrollView()
        scroll.add_widget(self.recipe_list)
        
        self.layout.add_widget(self.header)
        self.layout.add_widget(search_layout)
        self.layout.add_widget(scroll)
        self.layout.add_widget(self.selected_meals_layout)
        self.layout.add_widget(custom_layout)
        self.layout.add_widget(save_btn)
        
        self.add_widget(self.layout)
        
        self.selected_meal_list = []
    
    def on_pre_enter(self):
        self.title_label.text = f'Choisir un repas pour {self.day} ({self.get_meal_time_name()})'
        self.load_recipes()
        self.load_selected_meals()
    
    def get_meal_time_name(self):
        if self.meal_time == 'breakfast':
            return 'Petit déjeuner'
        elif self.meal_time == 'lunch':
            return 'Déjeuner'
        elif self.meal_time == 'dinner':
            return 'Dîner'
        return ''
    
    def load_recipes(self):
        self.recipe_list.clear_widgets()
        
        if recipes_store.count() == 0:
            self.recipe_list.add_widget(Label(text='Aucune recette enregistrée', size_hint_y=None, height=40, color=AppColors.TEXT))
        else:
            for recipe_name in recipes_store.keys():
                recipe_btn = Button(text=recipe_name, size_hint_y=None, height=50, 
                                   background_color=AppColors.PRIMARY)
                recipe_btn.bind(on_press=lambda btn, name=recipe_name: self.select_recipe(name))
                self.recipe_list.add_widget(recipe_btn)
    
    def load_selected_meals(self):
        self.selected_meals.clear_widgets()
        self.selected_meal_list = []
        
        if menu_store.exists(self.day):
            day_data = menu_store.get(self.day)
            if self.meal_time in day_data and isinstance(day_data[self.meal_time], list):
                self.selected_meal_list = day_data[self.meal_time]
        
        for meal in self.selected_meal_list:
            self.add_meal_to_selected_list(meal)
    
    def add_meal_to_selected_list(self, meal_name):
        meal_layout = BoxLayout(size_hint_y=None, height=30)
        meal_label = Label(text=meal_name, color=AppColors.TEXT)
        remove_btn = Button(text='X', size_hint_x=None, width=30, 
                           background_color=AppColors.SECONDARY)
        remove_btn.bind(on_press=lambda btn, name=meal_name: self.remove_meal(name))
        
        meal_layout.add_widget(meal_label)
        meal_layout.add_widget(remove_btn)
        
        self.selected_meals.add_widget(meal_layout)
        self.selected_meals.height = len(self.selected_meal_list) * 30
    
    def filter_recipes(self, instance, value):
        self.recipe_list.clear_widgets()
        
        if not value:
            self.load_recipes()
            return
        
        value = value.lower()
        found = False
        
        for recipe_name in recipes_store.keys():
            if value in recipe_name.lower():
                recipe_btn = Button(text=recipe_name, size_hint_y=None, height=50, 
                                   background_color=AppColors.PRIMARY)
                recipe_btn.bind(on_press=lambda btn, name=recipe_name: self.select_recipe(name))
                self.recipe_list.add_widget(recipe_btn)
                found = True
        
        if not found:
            self.recipe_list.add_widget(Label(text='Aucune recette trouvée', size_hint_y=None, height=40, color=AppColors.TEXT))
    
    def select_recipe(self, recipe_name):
        if recipe_name not in self.selected_meal_list:
            self.selected_meal_list.append(recipe_name)
            self.add_meal_to_selected_list(recipe_name)
    
    def remove_meal(self, meal_name):
        if meal_name in self.selected_meal_list:
            self.selected_meal_list.remove(meal_name)
            self.load_selected_meals()  # Refresh the list
    
    def add_custom_meal(self, instance):
        meal = self.custom_input.text.strip()
        if meal and meal not in self.selected_meal_list:
            self.selected_meal_list.append(meal)
            self.add_meal_to_selected_list(meal)
            self.custom_input.text = ''
    
    def save_meals(self, instance):
        day_data = {}
        if menu_store.exists(self.day):
            day_data = menu_store.get(self.day)
        
        day_data[self.meal_time] = self.selected_meal_list
        menu_store.put(self.day, **day_data)
        
        self.go_back(None)
    
    def go_back(self, instance):
        self.manager.current = 'menu'

class ShoppingListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(ShoppingListScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title and back button
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(text='Retour', size_hint_x=None, width=100, 
                         background_color=AppColors.SECONDARY)
        back_btn.bind(on_press=self.go_back)
        title = Label(text='Liste de courses', color=AppColors.TEXT)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Shopping list
        self.shopping_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.shopping_list.bind(minimum_height=self.shopping_list.setter('height'))
        
        # Add item layout
        add_layout = BoxLayout(size_hint_y=None, height=50)
        self.item_input = TextInput(hint_text='Nouvel article', multiline=False)
        self.quantity_input = TextInput(hint_text='Quantité', multiline=False, size_hint_x=None, width=80)
        self.unit_input = TextInput(hint_text='Unité', multiline=False, size_hint_x=None, width=80)
        add_btn = Button(text='+', size_hint_x=None, width=50, 
                        background_color=AppColors.PRIMARY)
        add_btn.bind(on_press=self.add_item)
        
        add_layout.add_widget(self.item_input)
        add_layout.add_widget(self.quantity_input)
        add_layout.add_widget(self.unit_input)
        add_layout.add_widget(add_btn)
        
        scroll = ScrollView()
        scroll.add_widget(self.shopping_list)
        
        self.layout.add_widget(header)
        self.layout.add_widget(scroll)
        self.layout.add_widget(add_layout)
        
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        self.load_shopping_list()
    
    def load_shopping_list(self):
        self.shopping_list.clear_widgets()
        
        if shopping_list_store.count() == 0:
            self.shopping_list.add_widget(Label(text='Liste de courses vide', size_hint_y=None, height=40, color=AppColors.TEXT))
        else:
            for item in shopping_list_store.keys():
                details = shopping_list_store.get(item)
                
                item_layout = BoxLayout(size_hint_y=None, height=50)
                
                checkbox = CheckBox(active=details['checked'], size_hint_x=None, width=30)
                checkbox.bind(active=lambda cb, value, i=item: self.toggle_item(i, value))
                
                # Make quantity editable
                quantity_input = TextInput(text=str(details['quantity']), multiline=False, 
                                          size_hint_x=None, width=60)
                quantity_input.bind(text=lambda instance, value, i=item: self.update_quantity(i, value))
                
                unit_label = Label(text=details['unit'], size_hint_x=None, width=50, color=AppColors.TEXT)
                item_label = Label(text=item, halign='left', color=AppColors.TEXT)
                item_label.bind(size=item_label.setter('text_size'))
                
                delete_btn = Button(text='X', size_hint_x=None, width=40, 
                                   background_color=AppColors.SECONDARY)
                delete_btn.bind(on_press=lambda btn, i=item: self.delete_item(i))
                
                item_layout.add_widget(checkbox)
                item_layout.add_widget(item_label)
                item_layout.add_widget(quantity_input)
                item_layout.add_widget(unit_label)
                item_layout.add_widget(delete_btn)
                
                self.shopping_list.add_widget(item_layout)
    
    def toggle_item(self, item, value):
        if shopping_list_store.exists(item):
            details = shopping_list_store.get(item)
            shopping_list_store.put(item, quantity=details['quantity'], unit=details['unit'], checked=value)
    
    def update_quantity(self, item, value):
        if shopping_list_store.exists(item):
            details = shopping_list_store.get(item)
            shopping_list_store.put(item, quantity=value, unit=details['unit'], checked=details['checked'])
    
    def add_item(self, instance):
        item = self.item_input.text.strip()
        quantity = self.quantity_input.text.strip()
        unit = self.unit_input.text.strip()
        
        if item:
            shopping_list_store.put(item, quantity=quantity, unit=unit, checked=False)
            
            self.item_input.text = ''
            self.quantity_input.text = ''
            self.unit_input.text = ''
            
            self.load_shopping_list()
    
    def delete_item(self, item):
        if shopping_list_store.exists(item):
            shopping_list_store.delete(item)
            self.load_shopping_list()
    
    def go_back(self, instance):
        self.manager.current = 'home'

class RecipeApp(App):
    def build(self):
        # Set window size for testing
        Window.size = (400, 600)
        
        # Set app colors
        self.title = 'Cuisine Assistant'
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RecipesScreen(name='recipes'))
        sm.add_widget(AddRecipeScreen(name='add_recipe'))
        sm.add_widget(ViewRecipeScreen(name='view_recipe'))
        sm.add_widget(EditRecipeScreen(name='edit_recipe'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ChooseMealScreen(name='choose_meal'))
        sm.add_widget(ShoppingListScreen(name='shopping'))
        
        return sm

if __name__ == '__main__':
    RecipeApp().run()