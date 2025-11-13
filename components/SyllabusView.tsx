import React from 'react';

const syllabusData = {
  general: [
    { title: "Tema 1: La Constitución Española de 1978", laws: [{ name: "Constitución Española", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }] },
    { title: "Tema 2: Derechos y deberes fundamentales", laws: [{ name: "Constitución Española (Título I)", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }] },
    { title: "Tema 3: El Tribunal Constitucional", laws: [{ name: "Ley Orgánica 2/1979, de 3 de octubre, del Tribunal Constitucional", url: "https://www.boe.es/eli/es/lo/1979/10/03/2" }] },
    { title: "Tema 4: La Corona. Funciones constitucionales del Rey", laws: [{ name: "Constitución Española (Título II)", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }] },
    { title: "Tema 5: El poder legislativo. Las Cortes Generales", laws: [{ name: "Constitución Española (Título III)", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }] },
    { title: "Tema 6: El Poder Judicial. El Consejo General del Poder Judicial", laws: [{ name: "Constitución Española (Título VI)", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }, { name: "Ley Orgánica 6/1985, de 1 de julio, del Poder Judicial", url: "https://www.boe.es/eli/es/lo/1985/07/01/6" }] },
    { title: "Tema 7: El poder ejecutivo. El Gobierno y las Cortes Generales", laws: [{ name: "Constitución Española (Título IV)", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }, { name: "Ley 50/1997, de 27 de noviembre, del Gobierno", url: "https://www.boe.es/eli/es/l/1997/11/27/50" }] },
    { title: "Tema 8: La Administración General del Estado", laws: [{ name: "Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público", url: "https://www.boe.es/eli/es/l/2015/10/01/40" }] },
    { title: "Tema 15: Los actos administrativos. Notificación y publicación", laws: [{ name: "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común", url: "https://www.boe.es/eli/es/l/2015/10/01/39" }] },
    { title: "Tema 21: Políticas de igualdad y contra la violencia de género", laws: [{ name: "Ley Orgánica 3/2007, para la igualdad efectiva de mujeres y hombres", url: "https://www.boe.es/eli/es/lo/2007/03/22/3" }, { name: "Ley Orgánica 1/2004, de Medidas de Protección Integral contra la Violencia de Género", url: "https://www.boe.es/eli/es/lo/2004/12/28/1" }] },
  ],
  specific: [
    { title: "Tema 1: La Seguridad Social en la Constitución Española de 1978. Texto Refundido de la LGSS", laws: [{ name: "Constitución Española (Art. 41)", url: "https://www.boe.es/legislacion/documentos/ConstitucionCASTELLANO.pdf" }, { name: "Real Decreto Legislativo 8/2015, Ley General de la Seguridad Social", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
    { title: "Tema 2: Campo de aplicación y composición del sistema de la Seguridad Social. Regímenes y Sistemas Especiales.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título I, Capítulos II y III", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
    { title: "Tema 3: Normas sobre afiliación, altas, bajas y variaciones de datos.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS)", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }, { name: "Real Decreto 84/1996, Reglamento General sobre inscripción, afiliación, altas, bajas y variaciones de datos", url: "https://www.boe.es/eli/es/rd/1996/01/26/84" }] },
    { title: "Tema 4: La cotización a la Seguridad Social: Normas comunes y regímenes.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS)", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }, { name: "Real Decreto 2064/1995, Reglamento General sobre Cotización y Liquidación", url: "https://www.boe.es/eli/es/rd/1995/12/22/2064" }] },
    { title: "Tema 5 y 6: Gestión recaudatoria voluntaria y ejecutiva.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS)", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }, { name: "Real Decreto 1415/2004, Reglamento General de Recaudación de la Seguridad Social", url: "https://www.boe.es/eli/es/rd/2004/06/11/1415" }] },
    { title: "Tema 7: Acción protectora. Contingencias comunes y profesionales.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título II, Capítulo I", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
    { title: "Tema 8: Incapacidad temporal e Incapacidad permanente contributiva.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título II, Capítulos V y XIII", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
    { title: "Tema 9: Nacimiento y cuidado de menor. Riesgo durante el embarazo y la lactancia.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS)", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }, { name: "Real Decreto 295/2009", url: "https://www.boe.es/eli/es/rd/2009/03/06/295" }] },
    { title: "Tema 10: Jubilación en la modalidad contributiva.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título II, Capítulo XIII", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
    { title: "Tema 11: La protección por muerte y supervivencia.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título II, Capítulo XIV", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
    { title: "Tema 12: Prestaciones no contributivas y asistenciales. Ingreso Mínimo Vital.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título II, Cap. XV y Título VI", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }, { name: "Ley 19/2021, del Ingreso Mínimo Vital", url: "https://www.boe.es/eli/es/l/2021/12/20/19" }] },
    { title: "Tema 13: Recursos del sistema de la Seguridad Social.", laws: [{ name: "R.D. Legislativo 8/2015 (LGSS), Título III", url: "https://www.boe.es/eli/es/rdlg/2015/10/30/8" }] },
  ],
};

const SyllabusTopic: React.FC<{ title: string; laws: { name: string; url: string }[] }> = ({ title, laws }) => (
  <details className="bg-slate-50 dark:bg-slate-800 rounded-lg shadow-sm open:ring-2 open:ring-blue-500 transition">
    <summary className="p-4 font-semibold cursor-pointer text-slate-800 dark:text-slate-100">{title}</summary>
    <div className="p-4 border-t border-slate-200 dark:border-slate-700">
      <h4 className="font-semibold mb-2 text-slate-600 dark:text-slate-300">Legislación Clave:</h4>
      <ul className="list-disc pl-5 space-y-1">
        {laws.map((law, index) => (
          <li key={index}>
            <a href={law.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 dark:text-blue-400 hover:underline">
              {law.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  </details>
);


const SyllabusView: React.FC = () => {
  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900">
      <header className="p-4 border-b border-slate-200 dark:border-slate-800">
        <h1 className="text-xl font-bold text-slate-800 dark:text-slate-100">Temario Oficial</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Cuerpo Administrativo de la Admón. de la Seguridad Social (Promoción Interna y Acceso Libre).</p>
      </header>
      <div className="flex-1 overflow-y-auto p-6 lg:p-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <div>
            <h2 className="text-2xl font-bold mb-4 text-slate-800 dark:text-slate-100 border-b-2 border-blue-500 pb-2">Temario General</h2>
            <div className="space-y-3">
              {syllabusData.general.map((topic, index) => (
                <SyllabusTopic key={`general-${index}`} title={topic.title} laws={topic.laws} />
              ))}
            </div>
          </div>
          <div>
            <h2 className="text-2xl font-bold mb-4 text-slate-800 dark:text-slate-100 border-b-2 border-blue-500 pb-2">Temario Específico Seguridad Social</h2>
            <div className="space-y-3">
               {syllabusData.specific.map((topic, index) => (
                <SyllabusTopic key={`specific-${index}`} title={topic.title} laws={topic.laws} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SyllabusView;