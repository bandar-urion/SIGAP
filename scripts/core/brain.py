import re
import pandas as pd

class Transaccion:
    def __init__(self, fecha, referencia, descripcion, monto, id_mp):
        self.idx = 0
        self.fecha_fmt = pd.to_datetime(fecha, dayfirst=True).strftime('%Y-%m-%d')
        self.referencia = str(referencia)
        self.descripcion_original = str(descripcion).strip()
        self.monto = float(monto)
        self.id_mp = id_mp
        self.descripcion_final = self.descripcion_original
        self.estado = 'PENDIENTE'
        self.id_cc = None; self.nombre_cc = "---"
        self.id_cat = None; self.nombre_cat = "---"
        self.id_subcat = None; self.nombre_subcat = "---"
        self.ia_match = False
        self.nuevo_sinonimo = None
        self.cuota_actual = 0; self.cuotas_totales = 0
        self.detectar_cuotas()

    def detectar_cuotas(self):
        texto = self.descripcion_original.upper()
        texto_limpio = re.sub(r'\b(DEL|AL|VTO|FECHA)\s+\d{1,2}[\/-]\d{1,2}([\/-]\d{2,4})?', ' ', texto)
        match = re.search(r'\b(\d{1,2})[\/](\d{1,2})\b(?!\/)', texto_limpio)
        if not match:
            match = re.search(r'(?:CTA|CUOTA)\s?(\d{1,2})', texto_limpio)
            if match:
                self.cuota_actual = int(match.group(1)); return
        if match:
            try:
                c_act, c_tot = int(match.group(1)), int(match.group(2))
                if c_act <= c_tot and c_tot <= 60:
                    self.cuota_actual, self.cuotas_totales = c_act, c_tot
            except: pass

def limpiar_texto(texto):
    basura = ["Compra con tarjeta de debito", "Transferencia realizada", "Transferencia recibida",
              "Pago de servicios", "Debito directo", "Su pago en", "Pago DEBIN", "\t"]
    limpio = texto
    for b in basura: limpio = limpio.replace(b, "").replace(b.upper(), "")
    limpio = " ".join(limpio.split())
    if limpio.startswith("-"): limpio = limpio[1:].strip()
    return limpio

def reanalizar_inteligencia(lista_tx, cursor, map_prefs_cc=None):
    """Aplica el diccionario de la DB a la lista de transacciones."""
    # Cargamos diccionario
    diccionario = cursor.execute("""
        SELECT d.termino, s.id, s.nombre, c.nombre, c.id
        FROM diccionario_terminos d
        JOIN param_subcategorias s ON d.id_subcategoria = s.id
        JOIN param_categorias c ON s.id_categoria = c.id
    """).fetchall()

    diccionario.sort(key=lambda x: len(x[0]), reverse=True)

    for tx in lista_tx:
        if tx.estado in ['DESCARTADO', 'LISTO', 'AUTO']: continue
        desc_visual_lower = limpiar_texto(tx.descripcion_original).lower()

        for termino, id_sub, nom_sub, nom_cat, id_cat in diccionario:
            if termino.lower() in desc_visual_lower:
                tx.id_subcat, tx.nombre_subcat = id_sub, nom_sub
                tx.nombre_cat, tx.id_cat = nom_cat, id_cat
                tx.ia_match = True

                # Intentar CC por defecto
                if map_prefs_cc and id_sub in map_prefs_cc:
                    tx.id_cc, tx.nombre_cc = map_prefs_cc[id_sub]
                    tx.estado = 'AUTO'
                break
