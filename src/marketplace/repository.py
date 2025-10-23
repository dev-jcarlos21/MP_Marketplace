from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Order, Product, Seller


class InMemoryRepo:
    """
    Repositorio en memoria. Carga datos desde archivos locales.
    No hay conexión a bases de datos ni APIs.
    """

    def __init__(self) -> None:
        self.products: dict[str, Product] = {}
        self.sellers: dict[str, Seller] = {}
        self.orders: dict[str, Order] = {}

    # TODO-1: Implementar carga de productos desde CSV (usar pydantic para validar)
    def load_products_csv(self, path: str | Path) -> int:
        count = 0
        line_number = 0

        with open(path, newline="", encoding="utf-8") as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)

            for fila in lector_csv:
                line_number += 1
                try:
                    # Intenta validar los datos con Pydantic
                    producto = Product(**fila)

                    # Validación para evitar SKUs duplicados
                    if producto.sku in self.products:
                        print(f"Advertencia línea {line_number}: SKU duplicado '{producto.sku}'")
                        continue

                    # Guarda en el diccionario usando el sku como clave
                    self.products[producto.sku] = producto
                    count += 1

                # Validacion en caso de error
                except Exception as e:
                    print(f"Error inesperado en línea {line_number}: {type(e).__name__}: {e}")
                    print(f"Datos de la fila: {fila}")

        # Devuelve cuántos productos fueron cargados
        return count

    # TODO-2: Implementar carga de sellers desde JSON (lista)
    def load_sellers_json(self, path: str | Path) -> int:
        count = 0
        error_count = 0

        try:
            # Lee el archivo JSON
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error al leer el archivo JSON: {e}")
            return 0

        for index, item in enumerate(data, start=1):
            try:
                # Validacion de datos con Pydantic
                seller = Seller(**item)

                # Validacion de duplicados
                if seller.seller_id in self.sellers:
                    print(f"Advertencia línea {index}: Seller duplicado '{seller.seller_id}'")
                    continue
                self.sellers[seller.seller_id] = seller
                count += 1
            except Exception as e:
                error_count += 1
                print(f"Error en item {index}: {type(e).__name__} - {e}")
                print(f"Datos problemáticos: {item}")
        # Devuelve cantidad de sellers cargados
        return count

    # TODO-3: Implementar carga de orders desde JSON (lista)
    def load_orders_json(self, path: str | Path) -> int:
        count = 0
        error_count = 0

        try:
            # Lee el archivo JSON
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error al leer el archivo JSON: {e}")
            return 0

        for index, item in enumerate(data, start=1):
            try:

                # Validacion de datos con Pydantic
                order = Order(**item)

                # Validacion de duplicados
                if order.order_id in self.orders:
                    print(f"Advertencia línea {index}: Seller duplicado '{order.order_id}'")
                    continue
                self.orders[order.order_id] = order
                count += 1
            except Exception as e:
                error_count += 1
                print(f"Error en item {index}: {type(e).__name__} - {e}")
                print(f"Datos problemáticos: {item}")
        # Devuelve cantidad de sellers cargados
        return count

    # TODO-4: Búsqueda segura de producto
    def get_product(self, sku: str) -> Product | None:
        producto = self.products.get(sku)

        # Validacion de existencia de producto
        if producto is None:
            print(f"Producto no encontrado: {sku}")
            return None

        return producto

    # TODO-5: Reporte simple de inventario agotado (stock == 0)
    def out_of_stock(self) -> list[Product]:
        return [product for product in self.products.values() if product.stock == 0]
