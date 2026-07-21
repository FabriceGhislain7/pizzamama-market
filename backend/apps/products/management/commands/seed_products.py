"""
Management command per popolare il DB con dati demo.

Uso:
    python manage.py seed_products
    python manage.py seed_products --clear    # cancella prima i dati esistenti
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.products.models import Category, PizzaSize, Pizza, Ingredient, Allergen, PizzaIngredient


ALLERGENS = [
    {"name": "Glutine", "symbol": "G", "description": "Cereali contenenti glutine"},
    {"name": "Latticini", "symbol": "L", "description": "Latte e derivati"},
    {"name": "Uova", "symbol": "U", "description": "Uova e prodotti a base di uova"},
    {"name": "Frutta a guscio", "symbol": "F", "description": "Noci, nocciole, mandorle ecc."},
    {"name": "Arachidi", "symbol": "A", "description": "Arachidi e prodotti a base di arachidi"},
]

CATEGORIES = [
    {"name": "Classiche", "description": "Le pizze della tradizione napoletana"},
    {"name": "Speciali", "description": "Creazioni dello chef con ingredienti ricercati"},
    {"name": "Vegetariane", "description": "Pizze senza carne, ricche di verdure fresche"},
    {"name": "Piccanti", "description": "Per chi ama il fuoco — con peperoncino doc"},
]

SIZES = [
    {"name": "Media", "diameter_cm": 28, "price_multiplier": "1.00"},
    {"name": "Grande", "diameter_cm": 32, "price_multiplier": "1.30"},
    {"name": "Maxi", "diameter_cm": 40, "price_multiplier": "1.70"},
]

INGREDIENTS = [
    {"name": "Pomodoro San Marzano", "cost_per_unit": "0.50", "price_per_extra": "1.00", "stock_quantity": 200},
    {"name": "Mozzarella fior di latte", "cost_per_unit": "1.20", "price_per_extra": "1.50", "stock_quantity": 150},
    {"name": "Basilico fresco", "cost_per_unit": "0.20", "price_per_extra": "0.50", "stock_quantity": 300},
    {"name": "Olio extravergine d'oliva", "cost_per_unit": "0.30", "price_per_extra": "0.50", "stock_quantity": 500},
    {"name": "Prosciutto crudo", "cost_per_unit": "1.80", "price_per_extra": "2.50", "stock_quantity": 80},
    {"name": "Funghi porcini", "cost_per_unit": "1.50", "price_per_extra": "2.00", "stock_quantity": 60},
    {"name": "Olive nere", "cost_per_unit": "0.60", "price_per_extra": "1.00", "stock_quantity": 120},
    {"name": "Cipolla rossa", "cost_per_unit": "0.40", "price_per_extra": "0.80", "stock_quantity": 200},
    {"name": "Peperoni grigliati", "cost_per_unit": "0.70", "price_per_extra": "1.20", "stock_quantity": 100},
    {"name": "Salsiccia calabrese", "cost_per_unit": "1.60", "price_per_extra": "2.00", "stock_quantity": 70},
    {"name": "Gorgonzola", "cost_per_unit": "1.40", "price_per_extra": "1.80", "stock_quantity": 50},
    {"name": "Rucola fresca", "cost_per_unit": "0.40", "price_per_extra": "0.80", "stock_quantity": 180},
    {"name": "Scamorza affumicata", "cost_per_unit": "1.30", "price_per_extra": "1.80", "stock_quantity": 60},
    {"name": "Nduja calabrese", "cost_per_unit": "1.70", "price_per_extra": "2.20", "stock_quantity": 40},
    {"name": "Mortadella Bologna IGP", "cost_per_unit": "1.20", "price_per_extra": "2.00", "stock_quantity": 70},
    {"name": "Zucchine grigliate", "cost_per_unit": "0.60", "price_per_extra": "1.00", "stock_quantity": 90},
    {"name": "Pomodorini ciliegino", "cost_per_unit": "0.50", "price_per_extra": "1.00", "stock_quantity": 150},
    {"name": "Pecorino romano", "cost_per_unit": "1.10", "price_per_extra": "1.50", "stock_quantity": 80},
]

PIZZAS = [
    {
        "name": "Margherita",
        "category": "Classiche",
        "base_price": "7.50",
        "short_description": "La classica napoletana con pomodoro e mozzarella",
        "description": "La regina delle pizze: pomodoro San Marzano, mozzarella fior di latte e basilico fresco. Semplice, autentica, insuperabile.",
        "is_featured": True,
        "ingredients": ["Pomodoro San Marzano", "Mozzarella fior di latte", "Basilico fresco", "Olio extravergine d'oliva"],
    },
    {
        "name": "Marinara",
        "category": "Classiche",
        "base_price": "6.50",
        "short_description": "Pomodoro, aglio e origano — niente formaggio",
        "description": "La pizza più antica di Napoli: pomodoro San Marzano, aglio, origano e olio. Vegana e piena di carattere.",
        "is_featured": False,
        "ingredients": ["Pomodoro San Marzano", "Basilico fresco", "Olio extravergine d'oliva"],
    },
    {
        "name": "Prosciutto e Funghi",
        "category": "Classiche",
        "base_price": "10.00",
        "short_description": "Prosciutto crudo e funghi porcini su base rossa",
        "description": "Un abbinamento intramontabile: prosciutto crudo di Parma e funghi porcini selezionati su base di pomodoro e mozzarella.",
        "is_featured": True,
        "ingredients": ["Pomodoro San Marzano", "Mozzarella fior di latte", "Prosciutto crudo", "Funghi porcini"],
    },
    {
        "name": "Quattro Stagioni",
        "category": "Classiche",
        "base_price": "11.00",
        "short_description": "Quattro guadrarti, quattro ingredienti diversi",
        "description": "Ogni spicchio racconta una stagione: prosciutto, funghi, olive e peperoni. Una pizza, quattro esperienze.",
        "is_featured": False,
        "ingredients": ["Pomodoro San Marzano", "Mozzarella fior di latte", "Prosciutto crudo", "Funghi porcini", "Olive nere", "Peperoni grigliati"],
    },
    {
        "name": "Diavola",
        "category": "Piccanti",
        "base_price": "9.50",
        "short_description": "Salsiccia piccante e nduja — per chi ama il fuoco",
        "description": "Non è per i deboli di cuore: salsiccia calabrese piccante, nduja spalmata e olio al peperoncino. Brucia bene.",
        "is_featured": True,
        "ingredients": ["Pomodoro San Marzano", "Mozzarella fior di latte", "Salsiccia calabrese", "Nduja calabrese"],
    },
    {
        "name": "Inferno",
        "category": "Piccanti",
        "base_price": "10.50",
        "short_description": "Tripla nduja, peperoni e cipolla rossa piccante",
        "description": "Il massimo della piccantezza: tripla dose di nduja, peperoni arrostiti, cipolla rossa e gocce di tabasco. Sfida accettata?",
        "is_featured": False,
        "ingredients": ["Pomodoro San Marzano", "Mozzarella fior di latte", "Nduja calabrese", "Peperoni grigliati", "Cipolla rossa"],
    },
    {
        "name": "Gorgonzola e Noci",
        "category": "Speciali",
        "base_price": "12.00",
        "short_description": "Crema di gorgonzola, noci e miele di acacia",
        "description": "Un contrasto sorprendente: gorgonzola cremoso, noci croccanti, miele di acacia e scamorza affumicata. Dolce-salato al massimo.",
        "is_featured": True,
        "ingredients": ["Mozzarella fior di latte", "Gorgonzola", "Scamorza affumicata"],
    },
    {
        "name": "Mortadella e Pistacchi",
        "category": "Speciali",
        "base_price": "13.00",
        "short_description": "Mortadella IGP, crema di pistacchi e rucola",
        "description": "Ispirazione siciliana: base bianca con mozzarella, mortadella Bologna IGP aggiunta a freddo, crema di pistacchi e rucola fresca.",
        "is_featured": True,
        "ingredients": ["Mozzarella fior di latte", "Mortadella Bologna IGP", "Rucola fresca"],
    },
    {
        "name": "Ortolana",
        "category": "Vegetariane",
        "base_price": "9.00",
        "short_description": "Verdure grigliate di stagione su base bianca",
        "description": "Un giardino in tavola: zucchine, peperoni, cipolla rossa e pomodorini ciliegino su base di mozzarella. Fresca e colorata.",
        "is_featured": False,
        "ingredients": ["Mozzarella fior di latte", "Zucchine grigliate", "Peperoni grigliati", "Cipolla rossa", "Pomodorini ciliegino"],
    },
    {
        "name": "Pugliese",
        "category": "Vegetariane",
        "base_price": "8.50",
        "short_description": "Olive, cipolla rossa e pomodorini — sapore del Sud",
        "description": "Profumi e sapori della Puglia: olive nere, cipolla rossa di Tropea, pomodorini e pecorino romano. Rustica e genuina.",
        "is_featured": False,
        "ingredients": ["Pomodoro San Marzano", "Mozzarella fior di latte", "Olive nere", "Cipolla rossa", "Pomodorini ciliegino", "Pecorino romano"],
    },
]


class Command(BaseCommand):
    help = "Popola il database con dati demo per prodotti (categorie, taglie, pizze)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Cancella tutti i prodotti esistenti prima di inserire i dati demo",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Cancellazione prodotti esistenti...")
            PizzaIngredient.objects.all().delete()
            Pizza.objects.all().delete()
            Ingredient.objects.all().delete()
            PizzaSize.objects.all().delete()
            Category.objects.all().delete()
            Allergen.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Prodotti cancellati."))

        # Allergeni
        self.stdout.write("Creazione allergeni...")
        allergen_map = {}
        for data in ALLERGENS:
            obj, _ = Allergen.objects.get_or_create(name=data["name"], defaults=data)
            allergen_map[data["name"]] = obj

        # Categorie
        self.stdout.write("Creazione categorie...")
        category_map = {}
        for data in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                name=data["name"],
                defaults={"description": data["description"]},
            )
            category_map[data["name"]] = obj
            if created:
                self.stdout.write(f"  + Categoria: {data['name']}")

        # Taglie
        self.stdout.write("Creazione taglie...")
        for data in SIZES:
            _, created = PizzaSize.objects.get_or_create(
                name=data["name"],
                defaults={
                    "diameter_cm": data["diameter_cm"],
                    "price_multiplier": data["price_multiplier"],
                },
            )
            if created:
                self.stdout.write(f"  + Taglia: {data['name']} ({data['diameter_cm']}cm)")

        # Ingredienti
        self.stdout.write("Creazione ingredienti...")
        ingredient_map = {}
        for data in INGREDIENTS:
            obj, created = Ingredient.objects.get_or_create(
                name=data["name"],
                defaults={
                    "cost_per_unit": data["cost_per_unit"],
                    "price_per_extra": data["price_per_extra"],
                    "stock_quantity": data["stock_quantity"],
                },
            )
            ingredient_map[data["name"]] = obj
            if created:
                self.stdout.write(f"  + Ingrediente: {data['name']}")

        # Pizze
        self.stdout.write("Creazione pizze...")
        pizza_count = 0
        for data in PIZZAS:
            category = category_map[data["category"]]
            pizza, created = Pizza.objects.get_or_create(
                name=data["name"],
                defaults={
                    "category": category,
                    "base_price": data["base_price"],
                    "short_description": data["short_description"],
                    "description": data["description"],
                    "is_featured": data["is_featured"],
                    "is_active": True,
                },
            )
            if created:
                pizza_count += 1
                # Aggiungi ingredienti
                for i, ing_name in enumerate(data.get("ingredients", [])):
                    if ing_name in ingredient_map:
                        PizzaIngredient.objects.get_or_create(
                            pizza=pizza,
                            ingredient=ingredient_map[ing_name],
                            defaults={"quantity": "1.00", "is_removable": i > 0},
                        )
                self.stdout.write(f"  + Pizza: {data['name']} ({data['base_price']}€)")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Seed completato: {len(CATEGORIES)} categorie, {len(SIZES)} taglie, "
            f"{len(INGREDIENTS)} ingredienti, {pizza_count} pizze create."
        ))
        if pizza_count == 0:
            self.stdout.write(self.style.WARNING(
                "Nessuna pizza creata — esistevano già. Usa --clear per ricominciare."
            ))
