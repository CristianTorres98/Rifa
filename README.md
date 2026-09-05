# Rifa 00-99

Proyecto sencillo de Streamlit + SQLite.

## Ejecutar en Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La base de datos esta creada en Supabase

## Archivos

- `app.py`: interfaz.
- `database.py`: Supabase.
- `boleto.py`: generación del PDF.
- `requirements.txt`: dependencias.
