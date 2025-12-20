#!/bin/bash
# Script para copiar Top 20 PDFs conceptuales

BASE_ESQUEMAS="/home/spas/OPOS_GEMINI_1/basura/del_ordenador/de_mi_hija/ESQUEMAS-20250327T124016Z-001/ESQUEMAS"
BASE_SS="/home/spas/OPOS_GEMINI_1/basura/del_ordenador/de_mi_hija/2024 opos ss y advo-20250327T124030Z-001/2024 opos ss y advo/SEGURIDAD SOCIAL LAS CORTES"
DEST="/home/spas/OPOS_GEMINI_1/conceptual_materials/pdfs"

echo "🔍 Copiando Top 20 PDFs conceptuales..."

# Esquemas Estructurales (10)
echo "📁 Esquemas Estructurales..."
cp "$BASE_ESQUEMAS/buenos/esquemaAAPPEE.pdf" "$DEST/01_esquemaAAPPEE.pdf"
cp "$BASE_ESQUEMAS/CE T VIII.pdf" "$DEST/02_CE_T_VIII.pdf"
cp "$BASE_ESQUEMAS/Instituciones ue.pdf" "$DEST/03_Instituciones_UE.pdf"
cp "$BASE_ESQUEMAS/T5 EL GOBIERNO y la admón.pdf" "$DEST/04_Gobierno_Admon.pdf"
cp "$BASE_ESQUEMAS/Tema 10 ent loc.pdf" "$DEST/05_Entidades_Locales.pdf"
cp "$BASE_ESQUEMAS/Tipos ENT LOC y sus órganos.pdf" "$DEST/06_Tipos_ENT_LOC.pdf"
cp "$BASE_ESQUEMAS/buenos/org congreso diputados T3.pdf" "$DEST/07_Org_Congreso.pdf"
cp "$BASE_ESQUEMAS/Delegados y subs gobierno.pdf" "$DEST/08_Delegados_Gobierno.pdf"
cp "$BASE_ESQUEMAS/buenos/CGPJ.pdf" "$DEST/09_CGPJ.pdf"
cp "$BASE_ESQUEMAS/buenos/Título VI CE EL PJ.pdf" "$DEST/10_Titulo_VI_PJ.pdf"

# Esquemas Procedimentales (5)
echo "⚙️  Esquemas Procedimentales..."
cp "$BASE_ESQUEMAS/PAC prinicpales PLAZOS.pdf" "$DEST/11_PAC_Plazos.pdf"
cp "$BASE_ESQUEMAS/buenos/L39-2015/Computo-de-plazos_esquema-general_easyleyes.pdf" "$DEST/12_Computo_Plazos.pdf"
cp "$BASE_ESQUEMAS/buenos/t7 bl I Acceso-a-informacion-publica-Ley-19-2013_easyleyes.pdf" "$DEST/13_Acceso_Info_Publica.pdf"
cp "$BASE_ESQUEMAS/buenos/t7 bl i Reclamacion-ante-el-Consejo-de-Transparencia-y-Buen-Gobierno_easyleyes.pdf" "$DEST/14_Reclamacion_Transparencia.pdf"
cp "$BASE_ESQUEMAS/buenos/LCSP plazos y procedimientos.pdf" "$DEST/15_LCSP_Plazos.pdf"

# Esquemas Comparativos (3)
echo "🔄 Esquemas Comparativos..."
cp "$BASE_ESQUEMAS/leyes ord leyes org rdl y dls.pdf" "$DEST/16_Leyes_Comparacion.pdf"
cp "$BASE_ESQUEMAS/Mayorías especiales exigidas CE.pdf" "$DEST/17_Mayorias_CE.pdf"
cp "$BASE_ESQUEMAS/buenos/Diferencia-decreto-ley-y-decreto-legistalivo_easyleyes.pdf" "$DEST/18_Diferencia_Decretos.pdf"

# Fichas y Resúmenes (2)
echo "📝 Fichas y Resúmenes..."
cp "$BASE_SS/FichaResumenSeguridadSocial2500PlazasAdvoC1.pdf" "$DEST/19_Ficha_SS.pdf"
cp "$BASE_ESQUEMAS/buenos/resumen_ley_3-2007.pdf" "$DEST/20_Resumen_Ley_3_2007.pdf"

echo ""
echo "✅ Copia completada!"
echo "📊 Verificando archivos..."
ls -lh "$DEST" | grep "\.pdf$" | wc -l
echo "archivos copiados"
