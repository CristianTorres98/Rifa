from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
import qrcode


def generar_boleto(numero, nombre, url_verificacion=None):
    # -----------------------------------------
    # CARPETA Y ARCHIVO
    # -----------------------------------------
    carpeta = Path("boletos")
    carpeta.mkdir(exist_ok=True)

    ruta = carpeta / f"boleto_{numero}.pdf"

    # -----------------------------------------
    # CONFIGURACIÓN DEL PDF
    # -----------------------------------------
    c = canvas.Canvas(str(ruta), pagesize=letter)
    ancho, alto = letter

    c.setTitle(f"Boleto Rifa Solidaria {numero}")
    c.setAuthor("Rifa Solidaria")

    # -----------------------------------------
    # COLORES
    # -----------------------------------------
    azul = colors.HexColor("#173B57")
    azul_claro = colors.HexColor("#EAF2F8")
    dorado = colors.HexColor("#C99A2E")
    gris = colors.HexColor("#555555")
    gris_claro = colors.HexColor("#F4F5F6")
    blanco = colors.white

    # -----------------------------------------
    # FONDO
    # -----------------------------------------
    c.setFillColor(colors.white)
    c.rect(0, 0, ancho, alto, fill=1, stroke=0)

    # -----------------------------------------
    # ENCABEZADO
    # -----------------------------------------
    c.setFillColor(azul)
    c.roundRect(
        25,
        alto - 150,
        ancho - 50,
        105,
        14,
        fill=1,
        stroke=0
    )

    # Línea dorada
    c.setFillColor(dorado)
    c.roundRect(
        25,
        alto - 154,
        ancho - 50,
        5,
        2,
        fill=1,
        stroke=0
    )

    # Título
    c.setFillColor(blanco)
    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(
        ancho / 2,
        alto - 85,
        "RIFA SOLIDARIA"
    )

    c.setFont("Helvetica", 11)
    c.drawCentredString(
        ancho / 2,
        alto - 108,
        "Un boleto que puede cambiar una vida"
    )

    # -----------------------------------------
    # PREMIO
    # -----------------------------------------
    c.setFillColor(dorado)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(
        ancho / 2,
        alto - 185,
        "PREMIO"
    )

    c.setFillColor(azul)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(
        ancho / 2,
        alto - 215,
        "TV DE 55 PULGADAS"
    )

    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(
        ancho / 2,
        alto - 238,
        ""
    )

    # -----------------------------------------
    # NÚMERO DEL BOLETO
    # -----------------------------------------
    c.setFillColor(azul_claro)
    c.roundRect(
        70,
        alto - 345,
        ancho - 140,
        75,
        12,
        fill=1,
        stroke=0
    )

    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(
        ancho / 2,
        alto - 292,
        "NÚMERO DE BOLETO"
    )

    c.setFillColor(azul)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(
        ancho / 2,
        alto - 328,
        str(numero)
    )

    # -----------------------------------------
    # NOMBRE
    # -----------------------------------------
    c.setFillColor(gris)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(
        ancho / 2,
        alto - 375,
        "PARTICIPANTE"
    )

    c.setFillColor(azul)
    c.setFont("Helvetica-Bold", 16)

    # Limitar nombres demasiado largos
    nombre_mostrar = str(nombre)

    if len(nombre_mostrar) > 38:
        nombre_mostrar = nombre_mostrar[:35] + "..."

    c.drawCentredString(
        ancho / 2,
        alto - 400,
        nombre_mostrar
    )

    # -----------------------------------------
    # QR
    # -----------------------------------------
    if url_verificacion:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2
        )

        qr.add_data(url_verificacion)
        qr.make(fit=True)

        qr_img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        qr_path = carpeta / f"qr_{numero}.png"
        qr_img.save(qr_path)

        # Dibujar QR
        c.drawImage(
            str(qr_path),
            ancho - 180,
            105,
            width=105,
            height=105,
            preserveAspectRatio=True,
            mask="auto"
        )

        c.setFillColor(gris)
        c.setFont("Helvetica", 8)
        c.drawCentredString(
            ancho - 127,
            92,
            "ESCANEA PARA VERIFICAR"
        )

    # -----------------------------------------
    # SECCIÓN DE AGRADECIMIENTO
    # -----------------------------------------
    c.setFillColor(gris_claro)
    c.roundRect(
        45,
        205,
        ancho - 90,
        125,
        12,
        fill=1,
        stroke=0
    )

    c.setFillColor(dorado)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(
        ancho / 2,
        303,
        "GRACIAS POR SER PARTE DE ESTA CAUSA"
    )

    c.setFillColor(gris)
    c.setFont("Helvetica", 9.5)

    texto = [
        "Tu participación representa una ayuda para el señor Oswaldo,",
        "un adulto mayor que actualmente se encuentra en situación de calle",
        "y que en estos momentos está hospedado en el",
        "Templo Cristiano Maranatha.",
        "",
        "C. Gral. Ernesto Ríos 7880, Revolución Mexicana,",
        "32670 Juárez, Chihuahua."
    ]

    y = 282

    for linea in texto:
        c.drawCentredString(
            ancho / 2,
            y,
            linea
        )
        y -= 13

    # -----------------------------------------
    # MENSAJE INSPIRADOR
    # -----------------------------------------
    c.setFillColor(azul)
    c.setFont("Helvetica-BoldOblique", 11)

    c.drawCentredString(
        ancho / 2,
        175,
        '"A veces, una pequeña ayuda puede convertirse'
    )

    c.drawCentredString(
        ancho / 2,
        160,
        'en una gran diferencia en la vida de alguien."'
    )

    # -----------------------------------------
    # MUCHA SUERTE
    # -----------------------------------------
    c.setFillColor(dorado)
    c.setFont("Helvetica-Bold", 15)

    c.drawCentredString(
        ancho / 2,
        130,
        "🍀 ¡MUCHA SUERTE EN LA RIFA! 🍀"
    )

    c.setFillColor(gris)
    c.setFont("Helvetica", 8.5)

    c.drawCentredString(
        ancho / 2,
        112,
        "Conserva este boleto como comprobante de participación."
    )

    c.drawCentredString(
        ancho / 2,
        98,
        "¡Gracias por ayudar y formar parte de esta iniciativa!"
    )

    # -----------------------------------------
    # PIE DE PÁGINA
    # -----------------------------------------
    c.setStrokeColor(colors.HexColor("#DDDDDD"))
    c.line(
        45,
        78,
        ancho - 45,
        78
    )

    c.setFillColor(colors.HexColor("#777777"))
    c.setFont("Helvetica", 7.5)

    c.drawCentredString(
        ancho / 2,
        62,
        f"Boleto #{numero} • Rifa Solidaria"
    )

    # -----------------------------------------
    # GUARDAR
    # -----------------------------------------
    c.save()

    # El QR temporal puede eliminarse después
    if url_verificacion:
        try:
            qr_path.unlink()
        except Exception:
            pass

    return ruta