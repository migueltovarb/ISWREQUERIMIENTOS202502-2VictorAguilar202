import funciones
import usuarios
import ventas

PRECIO_BOLETO = 10000

def guardar_modulo(nombre_modulo, datos, variable):
    with open(f"{nombre_modulo}.py", "w", encoding="utf-8") as f:
        f.write(f"{variable} = {datos}\n")


def registrar_usuario_y_compra():
    print("\n--- REGISTRO DE USUARIO ---")
    nombre = input("Ingrese su nombre completo: ")
    telefono = input("Ingrese su número de teléfono: ")
    correo = input("Ingrese su correo electrónico: ")

    for u in usuarios.lista_usuarios:
        if u["telefono"] == telefono or u["correo"] == correo:
            print("❌ Ya existe un usuario con ese teléfono o correo.")
            return

    nuevo_usuario = {"nombre": nombre, "telefono": telefono, "correo": correo}
    usuarios.lista_usuarios.append(nuevo_usuario)
    guardar_modulo("usuarios", usuarios.lista_usuarios, "lista_usuarios")
    print("✅ Usuario registrado correctamente.\n")

    # Mostrar funciones disponibles
    print("--- FUNCIONES DISPONIBLES ---")
    for f in funciones.lista_funciones:
        print(f"[{f['id']}] {f['pelicula']} - Hora: {f['hora']} - Precio: ${f['precio']}")
    print("-----------------------------")

    id_funcion = input("Ingrese el ID de la función que desea ver: ")
    funcion = next((f for f in funciones.lista_funciones if f["id"] == id_funcion), None)
    if not funcion:
        print("❌ La función ingresada no existe.")
        return

    try:
        cantidad = int(input("¿Cuántos boletos desea comprar?: "))
        if cantidad <= 0:
            print("❌ Cantidad inválida.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    total = cantidad * PRECIO_BOLETO
    print(f"\n🎟️ Has comprado {cantidad} boletos para '{funcion['pelicula']}'.")
    print(f"💰 Total a pagar: ${total}\n")

    nueva_venta = {
        "usuario": nombre,
        "id_funcion": id_funcion,
        "pelicula": funcion["pelicula"],
        "cantidad": cantidad,
        "total": total
    }
    ventas.lista_ventas.append(nueva_venta)
    guardar_modulo("ventas", ventas.lista_ventas, "lista_ventas")
    print("✅ Compra registrada exitosamente.\n")


def menu():
    while True:
        print("""
========= 🎬 CINE MOVIETIME =========
1. Registrar usuario y comprar boletos
2. Listar funciones disponibles
3. Ver resumen de ventas
4. Salir
======================================
""")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario_y_compra()
        elif opcion == "2":
            for f in funciones.lista_funciones:
                print(f"[{f['id']}] {f['pelicula']} - Hora: {f['hora']} - Precio: ${f['precio']}")
        elif opcion == "3":
            total_boletos = sum(v["cantidad"] for v in ventas.lista_ventas)
            total_dinero = sum(v["total"] for v in ventas.lista_ventas)
            print(f"\n--- RESUMEN DE VENTAS ---")
            print(f"Boletos vendidos: {total_boletos}")
            print(f"Dinero recaudado: ${total_dinero}\n")
        elif opcion == "4":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.\n")


if __name__ == "__main__":
    if not funciones.lista_funciones:
        funciones.lista_funciones = [
            {"id": "1", "pelicula": "Avengers: Endgame", "hora": "18:00", "precio": PRECIO_BOLETO},
            {"id": "2", "pelicula": "Spider-Man: No Way Home", "hora": "20:00", "precio": PRECIO_BOLETO},
            {"id": "3", "pelicula": "Interstellar", "hora": "22:00", "precio": PRECIO_BOLETO}
        ]
        guardar_modulo("funciones", funciones.lista_funciones, "lista_funciones")

    menu()
